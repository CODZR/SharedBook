#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from rest_framework.filters import BaseFilterBackend


class ReachBottomFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        min_id = request.query_params.get('minId')
        if not min_id:
            return queryset
        return queryset.filter(id__lt=min_id)


class PullDownRefreshFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        max_id = request.query_params.get('maxId')
        if not max_id:
            return queryset
        return queryset.filter(id__gt=max_id).reverse()


class BidItemFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        item_id = request.query_params.get('item_id')
        if not item_id:
            return queryset
        return queryset.filter(item_id=item_id)

class BookNameFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        title = request.query_params.get('title')
        if not title:
            return queryset
        return queryset.filter(title__contains=title)
class GoodBookFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        good = request.query_params.get('good')
        print(good)
        if not good:
            return queryset
        return queryset.order_by('-score')
    
class HotBookFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        hot = request.query_params.get('hot')
        print(hot)
        if not hot:
            return queryset
        return queryset.order_by('-borrowed_count')
    
    
    
class BookCheckedIdFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        checked_arr = request.query_params.get('checked_arr')
        if not checked_arr:
            return queryset
        return queryset.filter(id__in=json.loads(checked_arr))
    
    
class OrderStatusFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        selected = request.query_params.get('selected')
        
        # selected = {1: '全部订单', 2: '待支付', 3: '已支付', 4: '已取消'}
        if selected == "1" or not selected:
            return queryset
        if selected == "2" :
            return queryset.filter(order_status = 1)
        if selected == "3" :
            return queryset.filter(order_status = 2)
        if selected == "4" :
            return queryset.filter(order_status = 3)