#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/01 00:25
# @file:wechat.py
from django.conf import settings
from wechatpy import WeChatClient

from wechatpy.session.redisstorage import RedisStorage
from utils.redis import rd

session_interface = RedisStorage(rd, prefix="wechatpy")

wechat = WeChatClient(
    settings.WE_CHAT["APPID"], settings.WE_CHAT["APP_SECRET"], session=session_interface
)
