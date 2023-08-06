# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from django.dispatch import Signal

user_log = Signal(providing_args=["user_id", "metics", "model", "delta"], use_caching=True)