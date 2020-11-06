from django.urls import re_path

from apps.api.views import auction, book
from apps.api.views import auth
from apps.api.views import topic
from apps.api.views import news
from apps.api.views import auction
from apps.api.views import coupon
from apps.api.views import order

urlpatterns = [

    re_path(r'^msg/', auth.MessageView.as_view()),
    re_path(r'^login/', auth.LoginView.as_view()),
    re_path(r'^oss/credential/$', auth.OssCredentialView.as_view()),

    # 话题
    re_path(r'^topic/$', topic.TopicView.as_view()),
    re_path(r'^news/$', news.NewsView.as_view()),
    re_path(r'^news/(?P<pk>\d+)/$', news.NewsDetailView.as_view()),
    re_path(r'^news/favor/$', news.NewsFavorView.as_view()),
    re_path(r'^comment/$', news.CommentView.as_view()),
    re_path(r'^comment/favor/$', news.CommentFavorView.as_view()),
    re_path(r'^follow/$', news.FollowView.as_view()),
    
    # 图书
    re_path(r'^book/$', book.BookView.as_view()),
    re_path(r'^book/(?P<pk>\d+)/$', book.BookDetailView.as_view()),
    re_path(r'^evaluation/$', book.EvaluationView.as_view()),
    
    # 广告
    re_path(r'^ad/$', book.AdView.as_view()),
    # 拍卖
    # re_path(r'^auction/$', auction.AuctionView.as_view()),
    # re_path(r'^auction/(?P<pk>\d+)/$', auction.AuctionDetailView.as_view()),
    # re_path(r'^auction/deposit/(?P<pk>\d+)/$', auction.AuctionDepositView.as_view()),
    # re_path(r'^pay/deposit/$', auction.PayDepositView.as_view()),
    # re_path(r'^pay/deposit/notify/$', auction.PayDepositNotifyView.as_view()),
    # re_path(r'^bid/$', auction.BidView.as_view()),

    # 优惠券
    re_path(r'^coupon/$', coupon.CouponView.as_view()),
    re_path(r'^user/coupon/$', coupon.UserCouponView.as_view()),
    re_path(r'^choose/coupon/$', coupon.ChooseCouponView.as_view()),

    # 订单
    re_path(r'^cart/$', order.ShoppingCartView.as_view()),
    re_path(r'^order/$', order.OrderView.as_view()),
    re_path(r'^order/status/$', order.OrderStatusView.as_view()),
    
    
    re_path(r'^prepay/$', order.UnifiedOrderView.as_view()),
    re_path(r'^orderquery/$', order.OrderQueryView.as_view()),
    re_path(r'^paysuccess/$', order.PaySuccessView.as_view()),
    re_path(r'^pay/(?P<pk>\d+)/$', order.PayView.as_view()),
    re_path(r'^pay/now/$', order.PayNowView.as_view()),

    re_path(r'^address/$', order.AddressView.as_view()),

]
