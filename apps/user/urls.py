#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/02 14:38
# @file:urls.py
from rest_framework import routers
from apps.user import views

app_name = 'user'
router = routers.DefaultRouter()

router.register("user", views.UserViewSet, basename="user")

urlpatterns = router.urls
