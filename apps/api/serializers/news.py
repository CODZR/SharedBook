import collections
import itertools

from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend
from rest_framework import exceptions
from django.db.models import Max, F

from apps.api import models


# ################################ 动态列表 & 发布动态 ################################
class CreateNewsTopicModelSerializer(serializers.Serializer):
    key = serializers.CharField()
    cos_path = serializers.CharField()


class CreateNewsModelSerializer(serializers.ModelSerializer):
    imageList = CreateNewsTopicModelSerializer(many=True)
    
    class Meta:
        model = models.News
        exclude = ['user', 'viewer_count', 'comment_count']
    
    def create(self, validated_data):
        image_list = validated_data.pop('imageList')
        news_object = models.News.objects.create(**validated_data)
        data_list = models.NewsDetail.objects.bulk_create(
            [models.NewsDetail(**info, news=news_object) for info in image_list]
        )
        news_object.imageList = data_list
        if news_object.topic:
            models.Topic.objects.filter(id=news_object.topic_id).update(count=F('count') + 1)
        
        return news_object


class ListNewsModelSerializer(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = models.News
        exclude = ['address', ]
    
    def get_topic(self, obj):
        if not obj.topic:
            return
        return model_to_dict(obj.topic, ['id', 'title'])
    
    def get_user(self, obj):
        return model_to_dict(obj.user, ['id', 'nickname', 'avatar'])


# ################################ 动态详细 ################################
class RetrieveNewsDetailModelSerializerSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    viewer = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format='%Y-%m-%d')
    favor = serializers.SerializerMethodField()
    
    class Meta:
        model = models.News
        exclude = ['cover', ]
    
    def get_image_list(self, obj):
        return [model_to_dict(row, ['id', 'cos_path']) for row in obj.newsdetail_set.only('id', 'cos_path')]
    
    def get_topic(self, obj):
        if not obj.topic:
            return
        return model_to_dict(obj.topic, ['id', 'title'])
    
    def get_user(self, obj):
        context = model_to_dict(obj.user, ['id', 'nickname', 'avatar'])
        user_object = self.context['request'].user
        if not user_object:
            return context
        
        
        follow = user_object.follow.filter(id=obj.user_id).exists()
        context['follow'] = follow
        return context
    
    def get_favor(self, obj):
        user_object = self.context['request'].user
        if not user_object:
            return False
        return models.NewsFavorRecord.objects.filter(news=obj, user=user_object).exists()
    
    def get_viewer(self, obj):
        queryset = models.ViewerRecord.objects.filter(news=obj).order_by('-id')
        view_object_list = queryset[0:10].values('user_id', 'user__avatar')
        
        mapping = {
            'user_id': 'id',
            'user__avatar': 'avatar'
        }
        context = {
            'count': queryset.count(),
            'result': [{mapping[key]: value for key, value in row.items()} for row in view_object_list]
        }
        return context
    
    def get_comment(self, obj):
        news_comment_queryset = models.CommentRecord.objects.filter(news=obj)
        total_count = news_comment_queryset.count()
        
        mapping = {
            'id': 'id',
            'content': 'content',
            'create_date': 'create_date',
            'depth': 'depth',
            'user__nickname': "nickname",
            'user__avatar': "avatar",
            'reply_id': 'reply',
            'reply__user__nickname': "reply_nickname"
        }
        
        # 第一步： 获取前10条一级评论
        first_depth_queryset = news_comment_queryset.filter(depth=1).select_related('user', 'reply').order_by(
            '-id')[0:10].values(*mapping.keys())
        
        first_depth_dict = collections.OrderedDict()
        for row in first_depth_queryset:
            row['create_date'] = row['create_date'].strftime('%Y-%m-%d %H:%M')
            row_dict = {mapping[key]: value for key, value in row.items()}
            first_depth_dict[row['id']] = row_dict
        
        # 第二步：获取每个一级评论下的第一个二级评论的ID
        group_by_second_depth = news_comment_queryset.filter(depth=2, reply__in=first_depth_dict.keys()).values(
            'reply_id').annotate(max_id=Max('id'))
        second_depth_id_list = [item['max_id'] for item in group_by_second_depth]
        
        # 第三步：根据第二步获取二级评论，并将二级评论添加到一级评论的child中。
        second_depth_queryset = news_comment_queryset.filter(depth=2, id__in=second_depth_id_list).select_related(
            'user', 'reply').order_by('id').values(*mapping.keys())
        second_depth_dict = {}
        for row in second_depth_queryset:
            row['create_date'] = row['create_date'].strftime('%Y-%m-%d %H:%M')
            row_dict = {mapping[key]: value for key, value in row.items()}
            second_depth_dict[row['id']] = row_dict
            
            first_depth_dict[row_dict['reply']].setdefault('child', [])
            first_depth_dict[row_dict['reply']]['child'].append(row_dict)
        
        # 第四步：如果当前已赞过当前评论，则默认显示红色【已赞】
        user_object = self.context['request'].user
        if user_object:
            news_id = itertools.chain(first_depth_dict.keys(), second_depth_dict.keys())
            user_comment_favor_queryset = models.CommentFavorRecord.objects.filter(user=user_object,
                                                                                   comment_id__in=news_id)
            for item in user_comment_favor_queryset:
                if item.comment_id in first_depth_dict:
                    first_depth_dict[item.comment_id]['favor'] = True
                if item.comment_id in second_depth_dict:
                    second_depth_dict[item.comment_id]['favor'] = True
        
        context = {
            'count': total_count,
            'result': first_depth_dict.values()
        }
        return context


# ################################ 动态点赞 ################################
class NewsFavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NewsFavorRecord
        exclude = ['user', ]


# ################################ 动态评论 & 所有评论 ################################
class CommentModelSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    avatar = serializers.CharField(source='user.avatar', read_only=True)
    reply_nickname = serializers.CharField(source='reply.user.nickname', read_only=True)
    favor = serializers.SerializerMethodField()
    
    class Meta:
        model = models.CommentRecord
        exclude = ["favor_count", "user"]

    def get_user(self, obj):
        return model_to_dict(obj.user, fields=['id', 'nickname', 'avatar'])

    def get_favor(self, obj):
        user_object = self.context['request'].user
        if not user_object:
            return False
        return models.CommentFavorRecord.objects.filter(user_id=user_object.id, comment=obj).exists()


class ChildCommentFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        root_comment_id = request.query_params.get('root_id')

        if not root_comment_id:
            return queryset.none()
        return queryset.filter(root_id=root_comment_id).order_by("-id")


# ################################ 评论点赞 ################################
class FavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentFavorRecord
        exclude = ['user', ]


# ################################ 动态关注 ################################
class FollowSerializer(serializers.Serializer):
    user = serializers.IntegerField(label='要关注的用户ID')
    
    def validate_user(self, value):
        exists = models.UserInfo.objects.filter(id=value).exists()
        if not exists:
            raise exceptions.ValidationError('用户不存在')
        return value
