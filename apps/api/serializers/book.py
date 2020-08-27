from django.db.models import Avg
from django.forms import model_to_dict
from rest_framework import serializers

from apps.api import models
from utils.to_dict import my_model_to_dict


class BookModelSerializer(serializers.ModelSerializer):
	# status = serializers.SerializerMethodField()
	cover = serializers.CharField()
	
	class Meta:
		model = models.Book
		fields = ['id', 'title', 'cover', 'age', 'label']


class BookDetailModelSerializer(serializers.ModelSerializer):
	cover = serializers.CharField()
	score = serializers.SerializerMethodField()
	evaluation = serializers.SerializerMethodField()
	status = serializers.CharField(source="get_status_display")
	borrower = serializers.SerializerMethodField()
	
	
	class Meta:
		model = models.Book
		fields = '__all__'
	
	def get_score(self, obj):
		score = models.Evaluation.objects.filter(book=obj).aggregate(Avg('score'))['score__avg']
		if score:
			models.Book.objects.filter(pk=obj.id).update(score=score)
			return score
		return 0
	
		
	def get_borrower(self,obj):
		borrower_queryset = models.BorrowerRecord.objects.filter(book=obj).order_by('-id')[0:10]
		context = {
			'count': borrower_queryset.count(),
			'results': [model_to_dict(borrower_obj.user, ['avatar']) for borrower_obj in borrower_queryset]
		}
		return context
	
	def get_evaluation(self, obj):
		book_evaluation_queryset = models.Evaluation.objects.filter(book=obj).order_by(
			'-id')[0:10]  # 最近的10条
		evaluation_list = []
		for eval_obj in book_evaluation_queryset:
			evaluation_dict = model_to_dict(eval_obj, ['id', 'content'])
			evaluation_dict['create_date'] = eval_obj.create_date.strftime('%Y-%m-%d %H:%M:%S')
			evaluation_dict['score'] = eval_obj.score
			evaluation_dict['user'] = {}
			evaluation_dict['user']['nickname'] = eval_obj.user.nickname
			evaluation_dict['user']['avatar'] = eval_obj.user.avatar
			evaluation_list.append(evaluation_dict)
		context = {
			'count': book_evaluation_queryset.count(),
			'results': evaluation_list
		}

		return context
	
	

class ListEvaluationModelSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	
	class Meta:
		model = models.Evaluation
		fields = '__all__'
	
	def get_user(self, obj):
		return model_to_dict(obj.user, ['id', 'nickname', 'avatar'])


class CreateEvaluationModelSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	
	class Meta:
		model = models.Evaluation
		fields = '__all__'
	
	def get_user(self, obj):
		return model_to_dict(obj.user, ['id', 'nickname', 'avatar'])


class AdModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Ad
		fields = '__all__'
