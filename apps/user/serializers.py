#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/01 00:11
# @file:serializers.py
from django.utils import timezone
from rest_framework import serializers

from apps.draw.const import DrawHistoryStatusChoices
from apps.draw.models import DrawHistory
from apps.user import const
from apps.user.models import (
    User,
    AccountRecord,
    RechargeableCard,
    CarouselFigure,
    SignInDate,
)
from drf.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    is_nickname = serializers.SerializerMethodField(help_text="是否绑定微信昵称")
    shares_count = serializers.SerializerMethodField(help_text="分享次数")
    draw_count = serializers.SerializerMethodField(help_text="绘图次数")
    sign_in = serializers.SerializerMethodField(help_text="签到状态")

    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "avatar",
            "balance",
            "is_nickname",
            "shares_count",
            "draw_count",
            "sign_in",
        ]
        extra_kwargs = {
            "balance": {"read_only": True},
        }

    def get_is_nickname(self, obj) -> bool:
        return obj.nickname[:2] != "游客"

    def get_shares_count(self, obj) -> int:
        return AccountRecord.objects.filter(
            user=obj, reward_type=const.RewardTypeChoices.SHARE.value
        ).count()

    def get_draw_count(self, obj) -> int:
        return DrawHistory.objects.filter(
            user=obj, status=DrawHistoryStatusChoices.SUCCESS.value
        ).count()

    def get_sign_in(self, obj) -> bool:
        return not SignInDate.objects.filter(
            user=obj, date=timezone.now().date()
        ).exists()


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
