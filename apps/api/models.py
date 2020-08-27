from django.db import models


# ############################### 动态 ###############################

class UserInfo(models.Model):
    telephone = models.CharField(verbose_name='手机号', max_length=11)
    nickname = models.CharField(verbose_name='昵称', max_length=64)
    avatar = models.CharField(verbose_name='头像', max_length=64, null=True)
    token = models.CharField(verbose_name='用户Token', max_length=64)
    
    fans_count = models.PositiveIntegerField(verbose_name='粉丝个数', default=0)
    follow = models.ManyToManyField(verbose_name='关注', to='self', blank=True)
    
    balance = models.PositiveIntegerField(verbose_name='账户余额', default=1000)
    session_key = models.CharField(verbose_name='微信会话秘钥', max_length=32)
    openid = models.CharField(verbose_name='微信用户唯一标识', max_length=32)
    vip = models.OneToOneField(verbose_name='会员卡', to='Vip', on_delete= models.CASCADE,
                               null=True, blank=True, default=None)
    deposit = models.BooleanField(verbose_name='是否已缴纳押金', default=False)
    def __str__(self):
        return self.nickname


class Topic(models.Model):
    """
    话题
    """
    title = models.CharField(verbose_name='话题', max_length=32)
    count = models.PositiveIntegerField(verbose_name='关注度', default=0)


class News(models.Model):
    """
    动态
    """
    cover = models.CharField(verbose_name='封面', max_length=128)
    content = models.CharField(verbose_name='内容', max_length=255)
    topic = models.ForeignKey(verbose_name='话题', to='Topic', null=True, blank=True, on_delete=models.CASCADE)
    address = models.CharField(verbose_name='位置', max_length=128, null=True, blank=True)
    
    user = models.ForeignKey(verbose_name='发布者', to='UserInfo', related_name='news', on_delete=models.CASCADE)
    
    favor_count = models.PositiveIntegerField(verbose_name='赞数', default=0)
    # favor = models.ManyToManyField(verbose_name='点赞记录', to='UserInfo', related_name="news_favor")
    viewer_count = models.PositiveIntegerField(verbose_name='浏览数', default=0)
    # viewer = models.ManyToManyField(verbose_name='浏览器记录', to='UserInfo', related_name='news_viewer')
    comment_count = models.PositiveIntegerField(verbose_name='评论数', default=0)
    
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class ViewerRecord(models.Model):
    """
    浏览器记录
    """
    news = models.ForeignKey(verbose_name='动态', to='News', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)


class NewsFavorRecord(models.Model):
    """
    动态赞记录表
    """
    news = models.ForeignKey(verbose_name='动态', to='News', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='点赞用户', to='UserInfo', on_delete=models.CASCADE)


class CommentRecord(models.Model):
    """
    评论记录表
    """
    news = models.ForeignKey(verbose_name='动态', to='News', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    
    reply = models.ForeignKey(verbose_name='回复', to='self', null=True, blank=True, on_delete=models.CASCADE)
    depth = models.PositiveIntegerField(verbose_name='评论层级', default=1)
    
    favor_count = models.PositiveIntegerField(verbose_name='赞数', default=0)
    
    # 以后方便通过跟评论找到其所有的子孙评论
    root = models.ForeignKey(verbose_name='根评论', to='self', null=True, blank=True, related_name='descendant',
                             on_delete=models.CASCADE)


class CommentFavorRecord(models.Model):
    """
    评论赞记录
    """
    comment = models.ForeignKey(verbose_name='动态', to='CommentRecord', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='点赞用户', to='UserInfo', on_delete=models.CASCADE)


class NewsDetail(models.Model):
    """
    动态详细
    """
    key = models.CharField(verbose_name='腾讯对象存储中的文件名', max_length=128, help_text='用于以后在腾讯对象存储中删除')
    cos_path = models.CharField(verbose_name='腾讯对象存储中图片路径', max_length=128)
    news = models.ForeignKey(verbose_name='动态', to='News', on_delete=models.CASCADE)
    
    
# ############################### 广告 ###############################
class Ad(models.Model):
    """
    广告图片
    """
    key = models.CharField(verbose_name='腾讯对象存储中的文件名', max_length=128, help_text='用于以后在腾讯对象存储中删除')
    cos_path = models.CharField(verbose_name='腾讯对象存储中图片路径', max_length=128)


# ############################### 图书 ###############################
class Book(models.Model):
    """
    图书系列
    """
    title = models.CharField(verbose_name='书名', max_length=32)
    author = models.CharField(verbose_name='作者', max_length=32)
    press = models.CharField(verbose_name='出版社', max_length=32)
    label = models.CharField(verbose_name='标签', max_length=32)
    age = models.CharField(verbose_name='适宜岁数', max_length=32, default='3-6岁')
    score = models.DecimalField(verbose_name='综合评分', max_digits=2, decimal_places=1, default=0)
    status_choices = (
        (1, '仍有库存'),
        (2, '暂无存货'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    cover = models.CharField(verbose_name='封面', max_length=128)
    content = models.CharField(verbose_name='商品简介', max_length=255)
    remain_count = models.PositiveIntegerField(verbose_name='库存', default=1)
    borrowed_count = models.PositiveIntegerField(verbose_name='总借出次数', default=0)

class BookItem(models.Model):
    """
    图书（每一本）
    """
    book_num = models.CharField(verbose_name='专属编号', max_length=32)
    book = models.ForeignKey(verbose_name='图书', to='Book', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='所属用户', to='UserInfo',
                             on_delete=models.CASCADE, default=1)  # 默认图书属于管理员用户
    borrower_count = models.PositiveIntegerField(verbose_name='单本借出次数', default=0)
    borrowed = models.BooleanField(verbose_name='已借出', default=False)
    
    
class Evaluation(models.Model):
    """
    用户评价
    """
    book = models.ForeignKey(verbose_name='图书', to='Book', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评价内容', max_length=255)
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    score = models.DecimalField(verbose_name='评分', max_digits=2, decimal_places=1)
    create_date = models.DateTimeField(verbose_name='评价时间', auto_now_add=True)
    
class BorrowerRecord(models.Model):
    """
    动态借出记录表
    """
    book = models.ForeignKey(verbose_name='图书', to='Book', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    class Meta:
        unique_together = (("book", "user"),)


# ############################### 购物车 ###############################
class ShoppingCartRecord(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(verbose_name='图书', to='Book', on_delete=models.CASCADE, null=True, blank=True)
    checked = models.BooleanField(verbose_name='是否选中', default=False)

    
# class AuctionTask(models.Model):
#     """ 定时任务 """
#
#     preview_task = models.CharField(verbose_name='Celery预展任务ID', max_length=64)
#
#     auction_task = models.CharField(verbose_name='Celery拍卖任务ID', max_length=64)
#
#     auction_end_task = models.CharField(verbose_name='Celery拍卖结束任务ID', max_length=64)


class DepositRecord(models.Model):
    """ 押金 """
    status_choices = (
        (1, '未支付'),
        (2, '已支付')
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    
    uid = models.CharField(verbose_name='流水号', max_length=64)
    pay_type_choices = (
        (1, '微信'),
        (2, '余额')
    )
    pay_type = models.SmallIntegerField(verbose_name='支付方式', choices=pay_type_choices)
    
    amount = models.PositiveIntegerField(verbose_name='金额')  # 200
    
    user = models.OneToOneField(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    
    # 单品保证金则设置值，全场保证金，则为空
    

class Vip(models.Model):
    role_choice = (
        (1, '普通用户'),
        (2, '年卡会员'),
        (3, '月卡会员'),
        (4, '12次卡会员'),
    )
    role = models.PositiveSmallIntegerField(verbose_name="身份", choices=role_choice, default=1)
    book_count = models.PositiveSmallIntegerField(verbose_name="已借绘本数", default=0)
    deposit = models.ForeignKey(verbose_name="押金",to="DepositRecord",blank=True,
                                null=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

class Order(models.Model):
    """
    订单，拍卖结束时，执行定时任务处理：
        - 拍得，创建订单。
        - 未拍得，则退款到原账户
    """
    order_type_choices = (
        (1, '图书'),
        (2, '押金'),
        (3, '会员卡'),
    )
    order_type = models.PositiveSmallIntegerField(verbose_name='订单类型', choices=order_type_choices, default=1)
    order_status_choices = (
        (1, '待支付'),
        (2, '已支付'),
        (3, '已完成'),
        (4, '已取消'),
    )
    order_status = models.PositiveSmallIntegerField(verbose_name='订单状态', choices=order_status_choices, default=1)
    
    out_trade_no = models.CharField(verbose_name='商户订单号', max_length=32, default='')
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    order_array = models.CharField(verbose_name='订单列表', max_length=256, default='')
    price = models.PositiveIntegerField(verbose_name='价格')
    lend_date = models.CharField(verbose_name='借阅时间', max_length=32, default='')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    # twenty_four_task_id = models.CharField(verbose_name='24小时后定时任务', max_length=32, null=True, blank=True)
    
    # address = models.ForeignKey(verbose_name='收获地址', to='Address', null=True, blank=True, on_delete=models.CASCADE)
    
    pay_type_choices = (
        (1, '微信'),
        (2, '会员卡'),
        (3, '余额'),
    )
    pay_type = models.SmallIntegerField(verbose_name='支付方式', choices=pay_type_choices,
                                        null=True, blank=True, default=1)


class DepositRefundRecord(models.Model):
    """ 押金退款记录 """
    uid = models.CharField(verbose_name='流水号', max_length=64)
    status_choices = (
        (1, "待退款"),
        (2, '退款成功'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices)
    deposit = models.ForeignKey(verbose_name='押金', to='DepositRecord', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='退款金额')


class DepositDeduct(models.Model):
    """ 扣除保证金 """
    order = models.ForeignKey(verbose_name='订单', to='Order', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='金额')
    
    deduct_type_choices = (
        (1, '逾期扣款'),
        (2, '支付抵扣')
    )
    deduct_type = models.SmallIntegerField(verbose_name='扣款类型', choices=deduct_type_choices, default=1)


class Coupon(models.Model):
    """ 优惠券 """
    status_choices = (
        (1, '未开始'),
        (2, '领取中'),
        (3, '已结束')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    title = models.CharField(verbose_name='优惠券名称', max_length=32)
    
    money = models.PositiveIntegerField(verbose_name='抵扣金额', default=200)
    
    count = models.PositiveIntegerField(verbose_name='创建数量', default=100)
    apply_count = models.PositiveIntegerField(verbose_name='已申请数量', default=0)
    
    apply_start_date = models.DateTimeField(verbose_name='开始领取时间')
    apply_stop_date = models.DateTimeField(verbose_name='领取结束时间')
    
    apply_start_task_id = models.CharField(verbose_name='celery任务ID', max_length=64, null=True, blank=True)
    apply_stop_task_id = models.CharField(verbose_name='celery任务ID', max_length=64, null=True, blank=True)
    
    deleted = models.BooleanField(verbose_name='是否删除', default=False)


class UserCoupon(models.Model):
    status_choices = (
        (1, '未使用'),
        (2, '已使用'),
        (3, '已过期')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    coupon = models.ForeignKey(verbose_name='优惠券', to='Coupon', on_delete=models.CASCADE)
    order = models.ForeignKey(verbose_name='订单', to='Order', null=True, blank=True, on_delete=models.CASCADE)


class Address(models.Model):
    """ 地址 """
    name = models.CharField(verbose_name='收货人姓名', max_length=32)
    phone = models.CharField(verbose_name='联系电话', max_length=11)
    detail = models.CharField(verbose_name='收货地址', max_length=255)
    
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
