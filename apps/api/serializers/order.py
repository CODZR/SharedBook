import json

from rest_framework import serializers
from rest_framework import exceptions
from django.forms import model_to_dict
from apps.api import models


############################购物车###############################
class ShoppingCartModelSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    checked = serializers.BooleanField()
    
    class Meta:
        model = models.ShoppingCartRecord
        fields = ['book', 'checked']
    
    def get_book(self, obj):
        user_object = self.context['request'].user
        if obj.user == user_object:
             return model_to_dict(obj.book, fields=['id', 'title', 'cover'])
        return




class VipModelSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    
    class Meta:
        model = models.Vip
        fields = '__all__'
        

class OrderModelSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    price = serializers.IntegerField()
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    order_status = serializers.IntegerField()
    order_array = serializers.CharField()
    class Meta:
        model = models.Order
        fields = ['id','order_status','price', 'out_trade_no','lend_date', 'user','order_type', 'order_array','create_date']

        
class PayDepositModelSerializer(serializers.ModelSerializer):
    checked = serializers.BooleanField(default=False)

    class Meta:
        model = models.DepositRecord
        fields = ['id', 'amount', 'balance', 'checked']
 

class PayModelSerializer(serializers.ModelSerializer):
    user_balance = serializers.IntegerField(source='user.balance')

    # 拍品
    book = serializers.SerializerMethodField()

    # 保证金
    deposit = serializers.SerializerMethodField()

    # 是否有优惠券
    coupon = serializers.SerializerMethodField()

    # 支付方式
    pay_method = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        exclude = ['uid', 'user']

    def get_deposit(self, obj):
        return PayDepositModelSerializer(instance=obj.deposit).data

    def get_coupon(self, obj):
        user_object = self.context['request'].user
        exists = models.UserCoupon.objects.filter(
            user=user_object, status=1, coupon__auction=obj.item.auction_id).exists()

        context = {
            'id': None,
            'has': exists,
            'text': '请选择优惠券' if exists else '无',
            'money': 0
        }
        return context

    def get_pay_method(self, obj):
        balance = self.context['request'].user.balance
        info = {
            'selected': 1,
            'choices': [
                {'id': 1, 'text': '余额（%s）' % balance},
                {'id': 2, 'text': '微信支付'},
            ]
        }
        return info

    def get_book(self, obj):
        
        return {
            'title': obj.item.title,
            'cover': obj.item.cover.name,
            'uid': obj.item.uid
        }


class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        exclude = ['user' ]
