#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/05 22:27
# @file:stable_diffusion.py
from datetime import datetime

import requests

from utils.redis import rd
from utils.scheduler import Scheduler
from apps.draw.models import MachineLogs


class StableDiffusion:
    """Stable Diffusion模型"""

    def __init__(self):
        pass

    @staticmethod
    def generate_image(url, config, user):
        scheduler = Scheduler()
        machine = scheduler.get_machine()
        rd.set(machine.id, 1)
        start_time = datetime.now()
        response = requests.post(url=f"{machine.get_agreement_display()}://{machine.ip}:{machine.post}{url}",
                                 json=config.config, timeout=60)
        end_time = datetime.now()
        rd.set(machine.id, 0)
        total_time = f"{(end_time - start_time).seconds}秒"
        remark = f"用户:{user.username} 使用机器:{machine.name},请求:{url}, 花费时间:{total_time}。"
        MachineLogs.objects.create(machine=machine, user=user, config=config, remark=remark, total_time=total_time)
        return response.json()

