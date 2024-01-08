#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/05 21:58
# @file:utils.py

import random
from datetime import datetime

import arrow


def random_dict_from_list(lst):
    """
    Returns a random dictionary from a list of dictionaries
    """
    # Filter out the dictionaries from the list
    dicts = [item for item in lst if isinstance(item, dict)]

    # Return a random dictionary if there are any, else return None
    return random.choice(dicts) if dicts else None


def random_name():
    # 生成随机昵称
    now = datetime.now()
    name = now.strftime("%Y%m%d%H%M%S")
    return name


def local_timestamp():
    return arrow.utcnow().to("Asia/Shanghai").timestamp()


def make_key(key, key_prefix, version):
    return ":".join([key_prefix, str(version), key])

