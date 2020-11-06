"""
初始化动态表，在动态表中添加一些数据，方便操作
"""
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SharedBook.settings")
django.setup()

from apps.api import models


models.Evaluation.objects.create(
	content="快来看吧",
	score=4,
	book_id=1,
	user_id=1
)
models.Evaluation.objects.create(
	content="新书上架",
	score=5,
	book_id=1,
	user_id=1
)
models.Ad.objects.create(
	key="index_ad1.png",
	cos_path="https://ads-1300774580.cos.ap-nanjing.myqcloud.com/index_ad1.png",
)
models.Ad.objects.create(
	key="index_ad2.png",
	cos_path="https://ads-1300774580.cos.ap-nanjing.myqcloud.com/index_ad2.png",
)