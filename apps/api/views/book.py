from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from apps.api import models
from apps.api.serializers.book import BookModelSerializer, BookDetailModelSerializer, AdModelSerializer, \
    ListEvaluationModelSerializer,CreateEvaluationModelSerializer
from utils.auth import UserAuthentication
from utils.filters import ReachBottomFilter, PullDownRefreshFilter, BookNameFilter, BookCheckedIdFilter, GoodBookFilter, \
    HotBookFilter
from utils.pagination import RollLimitOffsetPagination


class BookView(ListAPIView):
    """ 图书列表接口 """
    queryset = models.Book.objects.exclude(status=2).order_by('-id')
    serializer_class = BookModelSerializer
    filter_backends = [ReachBottomFilter, PullDownRefreshFilter, BookNameFilter,
                       BookCheckedIdFilter, GoodBookFilter, HotBookFilter]
    pagination_class = RollLimitOffsetPagination
    

class BookDetailView(RetrieveAPIView):
    """ 图书详细接口 """
    queryset = models.Book.objects
    serializer_class = BookDetailModelSerializer


class EvaluationView(ListAPIView, CreateAPIView):
    """ 图书评论列表、发布接口 """
    queryset = models.Evaluation.objects
    
    def get_authenticators(self):
        if self.request.method == 'POST':
            print(UserAuthentication())
            return []
        return []
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListEvaluationModelSerializer
        if self.request.method == 'POST':
            return CreateEvaluationModelSerializer
       

class AdView(ListAPIView):
    queryset = models.Ad.objects
    serializer_class = AdModelSerializer
