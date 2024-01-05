#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/02 14:38
# @file:urls.py
from rest_framework import routers
from apps.draw import views

app_name = 'draw'
router = routers.DefaultRouter()

router.register("draw", views.DrawViewSet, basename="draw")

urlpatterns = router.urls
