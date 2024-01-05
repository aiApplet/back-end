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
router.register("signin", views.SignInViewSet, basename="signin")
router.register("account_record", views.AccountRecordViewSet, basename="account_record")
router.register("rechargeable_card", views.RechargeableCardViewSet, basename="rechargeable_card")

urlpatterns = router.urls
