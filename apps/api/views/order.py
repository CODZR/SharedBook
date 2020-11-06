import json
import time
import uuid

import requests
from django.db.models import F
from django.http import HttpResponse
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.views import APIView
from collections import OrderedDict
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from encoder import XML2Dict

from SharedBook.settings import WX_APPID, WX_SECRET, WX_MCH_ID
from apps.api import models
from utils.auth import UserAuthentication
from django.db import transaction
from rest_framework import exceptions
from rest_framework import status
from rest_framework.response import Response
from apps.api.serializers.order import OrderModelSerializer, PayModelSerializer, AddressModelSerializer, \
    ShoppingCartModelSerializer
from utils.filters import OrderStatusFilter
from utils.tencent import wxpay
from utils.tencent.wxpay import get_nonce_str, getWxPayOrderID


class ShoppingCartView(ListAPIView, CreateAPIView, DestroyAPIView):
    """ 购物车图书列表、增加至购物车接口 """
    authentication_classes = [UserAuthentication, ]
    serializer_class = ShoppingCartModelSerializer
    def get_queryset(self):
        return models.ShoppingCartRecord.objects.filter(user=self.request.user).order_by('id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = request.user.id
        book_id = request.data['book']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
        if models.ShoppingCartRecord.objects.filter(user_id=user_id, book_id=book_id):
            return Response(status=status.HTTP_202_ACCEPTED)
        serializer.save(user_id=self.request.user.id, book_id=self.request.data['book'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def delete(self, request, *args, **kwargs):
        deleted_list = request.data['deletedList']
        print(deleted_list)
        for book_id in deleted_list:
            print(book_id)
            print(request.user.id)
            models.ShoppingCartRecord.objects.get(book=book_id,user=request.user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookOrderView(ListAPIView):
    authentication_classes = [UserAuthentication, ]
    
    
class OrderView(ListAPIView,CreateAPIView,DestroyAPIView,UpdateAPIView):
    """ 订单接口 """
    authentication_classes = [UserAuthentication, ]
    filter_backends = [OrderStatusFilter]

    serializer_class = OrderModelSerializer
    
    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user).order_by('id')
    
    def post(self, request, *args, **kwargs):
        res_data = request.data
        if res_data['order_type'] == "1" and res_data['order_status']=="2":
            book_data = json.loads(res_data['order_array'])
            for item in book_data:
                models.BorrowerRecord.objects.create(user_id=self.request.user.id, book_id=item['id'])
                models.Book.objects.filter(pk=item['id']).update(borrowed_count=F('borrowed_count')+1)
        if res_data['order_type']=="2" and res_data['order_status']=="2":  # 押金订单且已支付
            models.UserInfo.objects.filter(pk=request.user.id).update(deposit=True)
        if res_data['order_type']=="3" and res_data['order_status']=="2":  # 会员订单且已支付
            print('vip开通成功')
            models.UserInfo.objects.filter(pk=request.user.id)
        print(request.data)

        # 并将订单数据保存到数据库
        order_serializer = OrderModelSerializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)
        print(order_serializer.errors)
        order_serializer.save()
        data = {"id": order_serializer.data['id'], "order_status":order_serializer.data['order_status']}
        return Response(data=data,status=HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        if request.data['order_type']==2 and request.data['order_status']==2:  # 押金订单且已支付
            models.UserInfo.objects.filter(pk=request.user.id).update(deposit=True)
            print('押金')
        instance = models.Order.objects.get(id=request.data['id'],user=request.data['user_id'])
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        print(serializer.errors)
        self.perform_update(serializer)
        return Response(data=serializer.data,status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        models.Order.objects.get(id=request.data['id']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UnifiedOrderView(APIView):
    """统一下单"""
    authentication_classes = [UserAuthentication, ]

    def post(self, request, *args, **kwargs):
        user_id = self.request.user.id
        if models.Order.objects.filter(user=user_id,order_status__in=[1,2]).count() > 1:
            return Response(status=HTTP_204_NO_CONTENT)
        # 获取价格
        price = int(request.data.get("price"))*100

        # 获取小程序用户唯一标识openid
        openid = models.UserInfo.objects.get(pk=request.user.id).openid
        out_trade_no = request.data['out_trade_no']
        print(out_trade_no)

        if out_trade_no is None:  # 如果未传入out_trade_no说明是新订单
            out_trade_no = getWxPayOrderID()  # 商户订单号
        
        # 请求微信的url
        order_url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

        # 拿到封装好的xml数据
        body_data = wxpay.get_bodyData(orderType='prepay', openid=openid, price=price, out_trade_no=out_trade_no)
        # 获取时间戳
        timestamp = str(int(time.time()))

        # 请求微信接口下单
        response = requests.post(order_url, body_data.encode("utf-8"), headers={'Content-Type': 'application/xml'})
        # 回复数据为xml,将其转为字典
        x = XML2Dict()
        content = x.parse(response.content)['xml']
        for key in content:
            content[key] = content[key].decode('UTF-8')
        print(content)

        if content['return_code'] == 'SUCCESS':
            # 获取预支付交易会话标识
            prepay_id = content['prepay_id']
            # 获取随机字符串
            nonceStr = content['nonce_str']
            
            # 获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
            paySign = wxpay.get_paysign(prepay_id, timestamp, nonceStr)
            # 封装返回给前端的数据
            data = {"prepay_id": prepay_id, "nonceStr": nonceStr, "paySign": paySign, "timestamp": timestamp,
                    "out_trade_no": out_trade_no}

            return Response(data, status=HTTP_200_OK)
    
        else:
            return HttpResponse("请求支付失败")


class OrderStatusView(APIView):
    """修改订单状态"""
    authentication_classes = [UserAuthentication, ]

    def post(self, request, *args, **kwargs):
        print(request.data)


class PaySuccessView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)


class OrderQueryView(APIView):
    """查询订单"""
    authentication_classes = [UserAuthentication, ]

    def post(self, request, *args, **kwargs):
        # 商户订单号
        # out_trade_no = request.data.get('out_trade_no')
        out_trade_no = '20200815143500475713'
        # 获取小程序用户唯一标识openid
        openid = models.UserInfo.objects.get(pk=request.user.id).openid
        # 请求微信的url
        order_url = "https://api.mch.weixin.qq.com/pay/orderquery"
        # 拿到封装好的xml数据
        body_data = wxpay.get_bodyData(orderType='queryset',out_trade_no=out_trade_no)

        # 请求微信接口下单
        response = requests.post(order_url, body_data.encode("utf-8"), headers={'Content-Type': 'application/xml'})
        # 回复数据为xml,将其转为字典
        x = XML2Dict()
        content = x.parse(response.content)['xml']
        print(content)

        if content['return_code'].decode('UTF-8') == 'SUCCESS':
            trade_state = content['trade_state'].decode('UTF-8')
            time_end = content['time_end'].decode('UTF-8')
            # 封装返回给前端的数据
            data = {'trade_state':trade_state, 'time_end':time_end}
            print(data)
            return Response(data, status=HTTP_200_OK)

        else:
            return HttpResponse("查询支付失败")


class PayView(RetrieveAPIView):
    authentication_classes = [UserAuthentication, ]
    # queryset = models.Order.objects.filter(status=1)
    serializer_class = PayModelSerializer

    def get_queryset(self):
        return models.Order.objects.filter(status=1,user=self.request.user)


class PayNowView(APIView):
    """ 立即支付 """
    authentication_classes = [UserAuthentication, ]
    
    def post(self, request, *args, **kwargs):
        print(request.data)
        # 1. 接收用户请求数据
        """
            {
                order_id: 1,
                coupon_id: 9, # 可以为空
                use_deposit: True/False # ,
                address_id: 1,
                real_pay: 100,
                pay_type: 1微信/2余额,

            }
        """
        order_id = request.data['order_id']
        address_id = request.data['address_id']
        real_pay = request.data['real_pay']
        pay_type = request.data['pay_type']
        
        deposit_deduct_object = None
        deposit_refund_object = None
        coupon_object = None
        
        # 2. 数据校验
        address_object = models.Address.objects.filter(user=request.user, id=address_id).first()
        if not address_object:
            raise exceptions.ValidationError('地址不存在')
        
        with transaction.atomic():
            # ## 2.1 订单是否合法？是否已经支付？
            order_object = models.Order.objects.filter(id=order_id, status=1,
                                                       user=request.user).select_for_update().first()
            if not order_object:
                raise exceptions.ValidationError('订单不存在')
            
            # 原价
            origin_price = order_object.price
            
            # 应该支付的价格
            real_price = order_object.price
            
            # ## 2.2 是否用优惠券
            if not coupon_id:
                # 不用优惠券
                pass
            else:
                # 用优惠券
                coupon_object = models.UserCoupon.objects.filter(id=coupon_id, user=request.user, status=1).first()
                if not coupon_object:
                    raise exceptions.ValidationError('优惠券不存在')
                
                if coupon_object.coupon.money > origin_price:
                    real_price = 0
                else:
                    real_price = origin_price - coupon_object.coupon.money
                
                # ---> bug: 优惠券更新为已使用 ? <----
                coupon_object.status = 2
                coupon_object.order = order_object
            
            # ## 2.3 是否用保证金？
            
            # ## 2.4 应付金额判断
            if real_pay != real_price:
                raise exceptions.ValidationError('前端和后端支付价格不一致')
            
            # 3.支付
            """
            if pay_type == 1:
                # 微信支付
                #   与支付订单的ID，签名给小程序返回json数据
                #   小程序中进行支付
                #       用户支付，
                #       用不不支付
                #   将订单和各种抵扣全都处理，但订单状态 先变更为 未支付，支付中，->已支付 （回调函数）
                pass
            else:
                # 余额支付
                pass
            """
            
            if request.user.balance < real_price:
                raise exceptions.ValidationError('余额不够，请充值')
            
            # 通过余额去支付
            request.user.balance = request.user.balance - real_price
            
            # 4. 数据更新
            # 对订单进行修改(带收货 -> 完成 )
            models.Order.objects.filter(id=order_object.id).update(real_price=real_price, pay_type=2, status=3,
                                                                   address_id=address_id)
            # 抵扣记录
            if deposit_deduct_object:
                deposit_deduct_object.save()
            # 退款记录
            if deposit_refund_object:
                deposit_refund_object.save()
            # 如果用了优惠券
            if coupon_object:
                coupon_object.save()
            # 余额退还
            request.user.save()
            
            # 此订单关联用户保证金余额提交数据（余额清空）
            order_object.deposit.save()
        
        return Response({}, status=status.HTTP_200_OK)

# class PayNowView(APIView):
#     """ 立即支付 """
#     authentication_classes = [UserAuthentication, ]
#
#     def post(self, request, *args, **kwargs):
#         print(request.data)
#         # 1. 接收用户请求数据
#         """
#             {
#                 order_id: 1,
#                 coupon_id: 9, # 可以为空
#                 use_deposit: True/False # ,
#                 address_id: 1,
#                 real_pay: 100,
#                 pay_type: 1微信/2余额,
#
#             }
#         """
#
#         order_id = request.data['order_id']
#         coupon_id = request.data['coupon_id']
#         use_deposit = request.data['use_deposit']
#         address_id = request.data['address_id']
#         real_pay = request.data['real_pay']
#         pay_type = request.data['pay_type']
#
#         deposit_deduct_object = None
#         deposit_refund_object = None
#         coupon_object = None
#
#         # 2. 数据校验
#         address_object = models.Address.objects.filter(user=request.user, id=address_id).first()
#         if not address_object:
#             raise exceptions.ValidationError('地址不存在')
#
#         with transaction.atomic():
#             # ## 2.1 订单是否合法？是否已经支付？
#             order_object = models.Order.objects.filter(id=order_id, status=1,
#                                                        user=request.user).select_for_update().first()
#             if not order_object:
#                 raise exceptions.ValidationError('订单不存在')
#
#             # 原价
#             origin_price = order_object.price
#
#             # 应该支付的价格
#             real_price = order_object.price
#
#             # ## 2.2 是否用优惠券
#             if not coupon_id:
#                 # 不用优惠券
#                 pass
#             else:
#                 # 用优惠券
#                 coupon_object = models.UserCoupon.objects.filter(id=coupon_id, user=request.user, status=1).first()
#                 if not coupon_object:
#                     raise exceptions.ValidationError('优惠券不存在')
#
#                 if coupon_object.coupon.money > origin_price:
#                     real_price = 0
#                 else:
#                     real_price = origin_price - coupon_object.coupon.money
#
#                 # ---> bug: 优惠券更新为已使用 ? <----
#                 coupon_object.status = 2
#                 coupon_object.order = order_object
#
#             # ## 2.3 是否用保证金？
#
#
#             # ## 2.4 应付金额判断
#             if real_pay != real_price:
#                 raise exceptions.ValidationError('前端和后端支付价格不一致')
#
#             # 3.支付
#             """
#             if pay_type == 1:
#                 # 微信支付
#                 #   与支付订单的ID，签名给小程序返回json数据
#                 #   小程序中进行支付
#                 #       用户支付，
#                 #       用不不支付
#                 #   将订单和各种抵扣全都处理，但订单状态 先变更为 未支付，支付中，->已支付 （回调函数）
#                 pass
#             else:
#                 # 余额支付
#                 pass
#             """
#
#             if request.user.balance < real_price:
#                 raise exceptions.ValidationError('余额不够，请充值')
#
#             # 通过余额去支付
#             request.user.balance = request.user.balance - real_price
#
#             # 4. 数据更新
#             # 对订单进行修改(带收货 -> 完成 )
#             models.Order.objects.filter(id=order_object.id).update(real_price=real_price, pay_type=2, status=3,
#                                                                    address_id=address_id)
#             # 抵扣记录
#             if deposit_deduct_object:
#                 deposit_deduct_object.save()
#             # 退款记录
#             if deposit_refund_object:
#                 deposit_refund_object.save()
#             # 如果用了优惠券
#             if coupon_object:
#                 coupon_object.save()
#             # 余额退还
#             request.user.save()
#
#             # 此订单关联用户保证金余额提交数据（余额清空）
#             order_object.deposit.save()
#
#         return Response({},status=status.HTTP_200_OK)


class AddressView(ListAPIView, CreateAPIView):
    authentication_classes = [UserAuthentication, ]
    serializer_class = AddressModelSerializer

    def get_queryset(self):
        return models.Address.objects.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DepositView(CreateAPIView):
    authentication_classes = [UserAuthentication, ]
