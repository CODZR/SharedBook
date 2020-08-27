from SharedBook.settings import WX_APPID, WX_MCH_ID, WX_MCH_KEY
import hashlib


def get_nonce_str():
    import uuid
    
    return uuid.uuid4().hex

# 生成签名的函数
def paysign(**params):
    ret = {}
    ret["appid"] = WX_APPID
    ret["mch_id"]= WX_MCH_ID
    ret["nonce_str"]= params['nonce_str']
    ret["out_trade_no"]= params['out_trade_no']
    if params['orderType']=='prepay':
        ret["body"] = params['body']
        ret["openid"] = params['openid']
        ret["notify_url"] = params['notify_url']
        ret["spbill_create_ip"]= params['spbill_create_ip']
        ret["total_fee"]= params['total_fee']
        ret["trade_type"]= 'JSAPI'

    # 处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
    stringA = '&'.join(["{0}={1}".format(k, ret.get(k)) for k in sorted(ret)])
    stringSignTemp = '{0}&key={1}'.format(stringA, WX_MCH_KEY)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()

def getWxPayOrderID():
    import datetime
    
    date = datetime.datetime.now()
    # 根据当前系统时间来生成商品订单号。时间精确到微秒
    return date.strftime("%Y%m%d%H%M%S%f")


#获取返回给小程序的paySign
def get_paysign(prepay_id,timeStamp,nonceStr):
    
    pay_data= {
        'appId': WX_APPID,
        'nonceStr': nonceStr,
        'package': "prepay_id="+prepay_id,
        'signType': 'MD5',
        'timeStamp':timeStamp
    }
    stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k))for k in sorted(pay_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA,WX_MCH_KEY)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()


# 获取全部参数信息，封装成xml,传递过来的openid和客户端ip，和价格需要我们自己获取传递进来
def get_bodyData(**params):
    body = '创阅读绘本馆'  # 商品描述
    notify_url = '127.0.0.1:8000/payMsg/'  # 填写支付成功的回调地址，微信确认支付成功会访问这个接口
    nonce_str = get_nonce_str()  # 随机字符串
    out_trade_no = params['out_trade_no']
    if params['orderType']=='prepay':
        openid = params['openid']
        spbill_create_ip = '106.53.21.189'
        total_fee = str(params['price'])  # 订单价格，单位是分


    # 获取签名
    sign = ''
    if params['orderType']=='prepay':
        sign = paysign(orderType='prepay',body=body, nonce_str=nonce_str, notify_url=notify_url,openid=openid ,
                       out_trade_no=out_trade_no, spbill_create_ip=spbill_create_ip, total_fee=total_fee)
    elif params['orderType']=='queryset':
        sign = paysign(orderType='queryset', nonce_str=nonce_str, out_trade_no=out_trade_no)
    bodyData = '<xml>'
    bodyData += '<appid>' + WX_APPID + '</appid>'  # 小程序ID
    bodyData += '<mch_id>' + WX_MCH_ID + '</mch_id>'  # 商户号
    bodyData += '<nonce_str>' + nonce_str + '</nonce_str>'  # 随机字符串
    bodyData += '<out_trade_no>' + out_trade_no + '</out_trade_no>'  # 商户订单号
    if params['orderType']=='prepay':
        bodyData += '<body>' + body + '</body>'
        bodyData += '<openid>' + openid + '</openid>'  # 用户标识
        bodyData += '<spbill_create_ip>' + spbill_create_ip + '</spbill_create_ip>'  # 客户端终端IP
        bodyData += '<notify_url>' + notify_url + '</notify_url>'  # 支付成功的回调地址
        bodyData += '<total_fee>' + total_fee + '</total_fee>'  # 总金额 单位为分
        bodyData += '<trade_type>JSAPI</trade_type>'  # 交易类型 小程序取值如下：JSAPI
    
    bodyData += '<sign>' + sign + '</sign>'
    bodyData += '</xml>'
    
    return bodyData

