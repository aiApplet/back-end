#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/01 00:25
# @file:redis.py
import django_redis

rd = django_redis.get_redis_connection("default")