
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from SharedBook.settings import COS_SECRET_ID, COS_SECRET_KEY, COS_BUCKET, COS_REGION


def upload_file(file_object, key, bucket=COS_BUCKET, region=COS_REGION):
    secret_id = COS_SECRET_ID  # 替换为用户的 secretId
    secret_key = COS_SECRET_KEY  # 替换为用户的 secretKey
    token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
    scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    # 2. 获取客户端对象
    client = CosS3Client(config)

    # 3. 上传文件
    response = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=file_object,
        Key=key
    )
    return "https://{0}.cos.{1}.myqcloud.com/{2}".format(bucket, region, key)
