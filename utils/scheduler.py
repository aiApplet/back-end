#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/12 19:00
# @file:scheduler.py
from apps.draw.models import Machines
from utils.redis import rd


class Scheduler:
    def __init__(self):
        self.machines = Machines.objects.filter(enabled=True)

    def get_machine(self):
        queue = {}
        for machine in self.machines:
            queue_name = f"rendering_{machine.id}"
            all_items = rd.lrange(queue_name, 0, -1)
            queue[machine] = len(all_items)
        min_machine = min(queue, key=lambda k: (queue[k], k))
        return min_machine

