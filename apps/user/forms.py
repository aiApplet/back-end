#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/01 00:12
# @file:forms.py
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user import const
from apps.user.models import User, SignInDate, AccountRecord, RechargeableCard
from rest_framework import serializers
from drf.serializers import ModelSerializer
from utils.wechat import wechat


class UserCreateForms(ModelSerializer):
    code = serializers.CharField(write_only=True)
    parent_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["code", "parent_id"]

    @staticmethod
    def validate_code(value):
        """
        验证code是否正确。
        你可以在这里添加你的验证逻辑，例如检查code是否匹配或是否有效。
        """
        try:
            user_data = wechat.wxa.code_to_session(value)
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return user_data

    def validate_parent_id(self, value):
        try:
            parent_user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("父用户不存在")
        return parent_user

    def create(self, validated_data):
        user_data = validated_data.pop("code", None)
        user, _ = User.objects.get_or_create(
            username=user_data["openid"], defaults={"password": make_password("123456")}
        )
        if _:
            parent_id = validated_data.get("parent_id")
            if parent_id:
                AccountRecord.objects.create(
                    user=parent_id,
                    amount=settings.SHARE_NEW_USER,
                    balance=parent_id.balance,
                    reward_type=const.RewardTypeChoices.SHARE.value,
                    remark=f"分享邀请新用户{user.id}，奖励积分:{settings.SHARE_NEW_USER}",
                )
        refresh = RefreshToken.for_user(user)
        return {"token": str(refresh.access_token)}


class SignInDateForms(ModelSerializer):
    class Meta:
        model = SignInDate
        fields = [
            "user",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def validate(self, attrs):
        user = self.context["request"].user
        if SignInDate.objects.filter(user=user, date=timezone.now().date()).exists():
            raise serializers.ValidationError("你今天已经签到了。")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.user.balance += settings.SIGN_IN_REWARD
        balance = instance.user.balance
        instance.user.save()
        AccountRecord.objects.create(
            user=instance.user,
            amount=settings.SIGN_IN_REWARD,
            balance=balance,
            reward_type=const.RewardTypeChoices.SIGN_IN.value,
            remark=f"签到获得{settings.SIGN_IN_REWARD}积分",
        )
        return instance


class RechargeableCardForms(ModelSerializer):
    class Meta:
        model = RechargeableCard
        fields = [
            "card_number",
        ]

    @transaction.atomic
    def create(self, validated_data):
        ModelClass = self.Meta.model
        instance = ModelClass._default_manager.filter(
            is_used=False, card_number=validated_data["card_number"]
        ).first()
        instance.is_used = True
        instance.use_time = datetime.now()
        instance.save()
        self.context["request"].user.balance += instance.amount
        self.context["request"].user.save()
        AccountRecord.objects.create(
            user=self.context["request"].user,
            amount=instance.amount,
            balance=self.context["request"].user.balance,
            reward_type=const.RewardTypeChoices.RECHARGE.value,
            remark=f"使用充值卡：{validated_data['card_number']}，充值{instance.amount}元",
        )
        return instance
