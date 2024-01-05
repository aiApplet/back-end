#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/02 14:38
# @file:urls.py
from django.urls import path
from rest_framework import routers
from apps.draw import views

app_name = 'draw'
router = routers.DefaultRouter()

router.register("draw", views.DrawViewSet, basename="draw")
router.register("prompts", views.PromptsViewSet, basename="prompts")
router.register("styles", views.StylesViewSet, basename="styles")
router.register("loras", views.LorasViewSet, basename="loras")
router.register("pictures", views.PicturesViewSet, basename="pictures")
router.register("user_like", views.UserLikeViewSet, basename="user_like")
router.register("user_comment", views.UserCommentViewSet, basename="user_comment")
urlpatterns = [
    path('random_prompts', views.RandomPromptViewSet.as_view(), name='random_prompts')
]
urlpatterns += router.urls
