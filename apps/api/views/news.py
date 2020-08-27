from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from apps.api import models
from apps.api.serializers.news import CreateNewsModelSerializer, ListNewsModelSerializer, \
    RetrieveNewsDetailModelSerializerSerializer, NewsFavorSerializer, CommentModelSerializer, ChildCommentFilter, \
    FavorSerializer, FollowSerializer
from utils.auth import UserAuthentication, GeneralAuthentication
from utils.filters import ReachBottomFilter, PullDownRefreshFilter


# ################################ 动态列表 & 发布动态 ################################
class NewsView(CreateAPIView, ListAPIView):
    """
    动态相关接口
        - 查看动态列表
        - 创建动态
    """
    queryset = models.News.objects.prefetch_related('user', 'topic').order_by("-id")
    
    filter_backends = [ReachBottomFilter, PullDownRefreshFilter]
    
    def get_authenticators(self):
        if self.request.method == 'POST':
            return [UserAuthentication(), ]
        return []
    
    def perform_create(self, serializer):
        new_object = serializer.save(user_id=self.request.user.id)
        return new_object
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateNewsModelSerializer
        if self.request.method == 'GET':
            return ListNewsModelSerializer


# ################################ 动态详细 ################################


class NewsDetailView(RetrieveAPIView):
    """
    获取动态详细接口
    """
    queryset = models.News.objects.all().order_by('-id')
    serializer_class = RetrieveNewsDetailModelSerializerSerializer
    
    def get(self, request, *args, **kwargs):
        # 1. 获取详细信息
        response = self.retrieve(request, *args, **kwargs)
            # 2. 处理用户浏览记录，当前用户添加到记录中
        #    2.1 用户未登录，不记录
        #    2.2 用户登录，已记录则不再记录记录，未记录则添加到浏览记录中。
        if not request.user:
            return response
        news_object = self.get_object()
        if not news_object:
            return response
        
        viewer_queryset = models.ViewerRecord.objects.filter(news=news_object, user_id=request.user.id)
        if not viewer_queryset.exists():
            models.ViewerRecord.objects.create(news=news_object, user_id=request.user.id)
            models.News.objects.filter(id=news_object.id).update(favor_count=F("viewer_count") + 1)
        
        return response


# ################################ 动态点赞 ################################


class NewsFavorView(APIView):
    serializer_class = NewsFavorSerializer
    authentication_classes = [UserAuthentication, ]
    
    def post(self, request, *args, **kwargs):
        """ 点赞和取消赞 """
        serializer = NewsFavorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        news_object = serializer.validated_data.get('news')
        queryset = models.NewsFavorRecord.objects.filter(news=news_object, user=request.user)
        if queryset.exists():
            queryset.delete()
            models.News.objects.filter(id=news_object.id).update(favor_count=F("favor_count") - 1)
            return Response({}, status=status.HTTP_200_OK)
        serializer.save(user_id=request.user.id)
        models.News.objects.filter(id=news_object.id).update(favor_count=F("favor_count") + 1)
        
        return Response({}, status=status.HTTP_201_CREATED)


# ################################ 动态评论 & 所有评论 ################################


class CommentView(ListAPIView, CreateAPIView):
    serializer_class = CommentModelSerializer
    queryset = models.CommentRecord.objects

    filter_backends = [ChildCommentFilter, ]

    def get_authenticators(self):
        if self.request.method == 'POST':
            return [UserAuthentication(), ]
        
        return [GeneralAuthentication(), ]
    
    
    
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
        news_object = serializer.validated_data.get('news')
        models.News.objects.filter(id=news_object.id).update(comment_count=F("comment_count") + 1)


# ################################ 评论点赞 ################################


class CommentFavorView(APIView):
    serializer_class = FavorSerializer
    authentication_classes = [UserAuthentication, ]
    
    def post(self, request, *args, **kwargs):
        """ 点赞和取消赞 """
        serializer = FavorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment_object = serializer.validated_data.get('comment')
        queryset = models.CommentFavorRecord.objects.filter(comment=comment_object, user_id=request.user.id)
        # 已存在，删除赞
        if queryset.exists():
            queryset.delete()
            models.CommentRecord.objects.filter(id=comment_object.id).update(favor_count=F("favor_count") - 1)
            return Response({}, status=status.HTTP_200_OK)
        # 不存在，创建赞
        serializer.save(user_id=request.user.id)
        models.CommentRecord.objects.filter(id=comment_object.id).update(favor_count=F("favor_count") + 1)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ################################ 动态关注 ################################


class FollowView(APIView):
    serializers = [UserAuthentication, ]
    
    def post(self, request, *args, **kwargs):
        """ 关注和取消关注：已关注则取消，未关注则关注"""
        ser = FollowSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        
        target_user_id = ser.validated_data.get('user')
        current_user_object = request.user
        
        exists = current_user_object.follow.filter(id=target_user_id).exists()
        if exists:
            # 已关注，则取消关注
            current_user_object.follow.remove(target_user_id)
            models.UserInfo.objects.filter(id=target_user_id).update(fans_count=F('fans_count') - 1)
            return Response({}, status=status.HTTP_200_OK)
        
        # 为关注，则关注
        current_user_object.follow.add(target_user_id)
        models.UserInfo.objects.filter(id=target_user_id).update(fans_count=F('fans_count') + 1)
        return Response({}, status=status.HTTP_201_CREATED)
