#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2023/11/08 14:59
# @file:permissions.py
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from rest_framework import permissions


class BalancePermission(permissions.BasePermission):

    message = "积分不足"

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.balance < settings.GEN_IMAGE_COST:
            return False
        return True
