from sts.sts import Sts

from SharedBook.settings import COS_SECRET_ID, COS_SECRET_KEY, COS_BUCKET, COS_REGION


def get_credential():
    config = {
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 1800,
        # 固定密钥 id
        'secret_id': COS_SECRET_ID,
        # 固定密钥 key
        'secret_key': COS_SECRET_KEY,
        # 换成你的 bucket
        'bucket': COS_BUCKET,
        # 换成 bucket 所在地区
        'region': COS_REGION,
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            'name/cos:PostObject',
            'name/cos:DeleteObject',
            # "name/cos:UploadPart",
            # "name/cos:UploadPartCopy",
            # "name/cos:CompleteMultipartUpload",
            # "name/cos:AbortMultipartUpload",
            # "*",
        ],

    }

    sts = Sts(config)
    response = sts.get_credential()
    return response


if __name__ == '__main__':
    get_credential()
