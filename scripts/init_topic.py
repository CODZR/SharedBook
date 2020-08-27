#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SharedBook.settings")
django.setup()

from apps.api import models

result = models.Topic.objects.bulk_create([
    models.Topic(title='图书'),
    models.Topic(title='孩子'),
    models.Topic(title='玩具'),
    models.Topic(title='日常'),
])
print(result)
