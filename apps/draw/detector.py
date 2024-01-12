#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/12 19:25
# @file:detector.py

from apps.draw.models import Machines
from utils.redis import rd

print("执行初始化机器状态")

machine_ids = Machines.objects.filter(enabled=True).values_list("id", flat=True)
for machine_id in machine_ids:
    status = rd.get(machine_id)
    if status is None:
        rd.set(machine_id, 0)
