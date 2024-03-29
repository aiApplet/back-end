#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/05 21:51
# @file:serializers.py
from rest_framework import serializers

from apps.draw.models import (
    PromptAssistant,
    DrawConfig,
    Styles,
    Loras,
    DrawHistory,
    UserLike,
    UserComment,
)
from drf.serializers import ModelSerializer


class DrawHistoryImageSerializer(ModelSerializer):
    class Meta:
        model = DrawHistory
        fields = ("image",)
        ref_name = "DrawHistoryImage"


class PromptAssistantSerializer(ModelSerializer):
    class Meta:
        model = PromptAssistant
        exclude = ("id",)


class StylesSerializer(ModelSerializer):
    class Meta:
        model = Styles
        exclude = ("sort", "style")


class LorasSerializer(ModelSerializer):
    class Meta:
        model = Loras
        fields = [
            "id",
            "name",
            "weight",
            "cover",
        ]


class DrawConfigTemplate(ModelSerializer):
    style_name = serializers.CharField(source="style.name", read_only=True)

    class Meta:
        model = DrawConfig
        exclude = ["config", "lora"]


class DrawHistorySerializer(ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)
    avatar = serializers.CharField(source="user.avatar", read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    config = DrawConfigTemplate(read_only=True)
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = DrawHistory
        exclude = (
            "status",
            "user",
        )

    def get_is_like(self, obj) -> bool:
        return obj.history_set.exists()


class UserLikeSerializer(ModelSerializer):
    class Meta:
        model = UserLike
        fields = ("id",)


class UserCommentSerializer(ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    is_author = serializers.SerializerMethodField()
    nickname = serializers.CharField(source="user.nickname", read_only=True)
    avatar = serializers.CharField(source="user.avatar", read_only=True)

    class Meta:
        model = UserComment
        fields = (
            "id",
            "content",
            "nickname",
            "avatar",
            "create_time",
            "is_author",
        )

    def get_is_author(self, obj) -> bool:
        """
        判断当前用户是否为评论作者
        """
        request = self.context["request"]
        return request.user == obj.user
