#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/01 00:11
# @file:serializers.py
from rest_framework import serializers

from apps.user.models import User, AccountRecord, RechargeableCard, CarouselFigure
from drf.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    is_nickname = serializers.SerializerMethodField(help_text="是否绑定微信昵称")

    class Meta:
        model = User
        fields = ["id", "nickname", "avatar", "balance", "is_nickname"]
        extra_kwargs = {
            "balance": {"read_only": True},
        }

    def get_is_nickname(self, obj) -> bool:
        return obj.nickname[:2] != "游客"

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance


class AccountRecordSerializer(ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = AccountRecord
        exclude = [
            "user",
        ]


class RechargeableCardSerializer(ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    use_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = RechargeableCard
        exclude = [
            "user",
        ]


class CarouselFigureSerializer(ModelSerializer):
    class Meta:
        model = CarouselFigure
        fields = ["id", "image", "link"]
