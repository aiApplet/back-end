#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/05 21:51
# @file:serializers.py
from rest_framework import serializers

from apps.draw.models import PromptAssistant, DrawConfig, Styles, Loras, DrawHistory, UserLike, UserComment
from drf.serializers import ModelSerializer


class DrawHistoryImageSerializer(ModelSerializer):
    class Meta:
        model = DrawHistory
        fields = ('image',)
        ref_name = "DrawHistoryImage"


class PromptAssistantSerializer(ModelSerializer):
    class Meta:
        model = PromptAssistant
        exclude = ('id',)


class StylesSerializer(ModelSerializer):
    class Meta:
        model = Styles
        exclude = ('sort', 'style')


class LorasSerializer(ModelSerializer):
    class Meta:
        model = Loras
        fields = ["id", "name", "weight", "cover", ]


class DrawHistorySerializer(ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)
    avatar = serializers.CharField(source="user.avatar", read_only=True)

    class Meta:
        model = DrawHistory
        exclude = ("status",)
        depth = 1


class UserLikeSerializer(ModelSerializer):
    class Meta:
        model = UserLike
        fields = ("id",)


class UserCommentSerializer(ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = UserComment
        fields = ("id", "content", "create_time",)
