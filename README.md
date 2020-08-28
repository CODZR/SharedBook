# SharedBook
共享绘本微信小程序的API接口(基于`python3.6.8`和`django3.0.7`)
## 主要功能：

- 绘本添加、查询（Max/MinIdFilter支持每次显示10本，下次从Max/MinId继续查询，NameFilter）接口
- 购物车添加、删除、查询接口
- 动态添加、查询、删除接口，腾讯云对象存储动态图片
- 动态相关评论添加（多级评论）、查询(显示更多)接口
- 订单（绘本、会员、押金3种类型的订单）添加、删除、查询（typeFilter）、修改接口
- 微信预（统一）下单、查询/关闭订单、退款接口及其相关算法代码
- 登录/注册接口，腾讯云短信
- 认证器、限流器、分页器、（反）序列化器等


##安装
> pip install -r requirements.txt

## 配置
因`WX/Cos_Secret_Key`等不可泄漏数据均配置在`settings.py`中,另准备了一份本地版的`settings2.py`，可根据自己需要配置
`ALLOWED_HOSTS,DATABASES,REST_FRAMEWORK`以及自己的
`COS_SECRET_ID，COS_SECRET_KEY，COS_BUCKET，COS_REGION，WX_APPID，WX_SECRET，WX_MCH_ID，WX_MCH_KEY`

## View的选择
以继承`GenericView`中的`List/RetriewAPIView、Create/Update/DeleteAPIView`为主，无需指定`get_queryset`或`obeject`的
如微信统一下单接口以`APIView`为主。
## Serializer的选择
涉及到模型操作多使用`ModelSerializer`，否则`Serializer`，需要展示复杂数据类型使用`SerializerMethodField`自定义该字段方法，如先判断再返回`model_to_dict(...)`
## 联系我
`qq:975336710`
`phone:13335913629`