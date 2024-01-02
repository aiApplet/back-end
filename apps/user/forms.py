#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/01 00:12
# @file:forms.py
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User, SignInDate, AccountRecord
from rest_framework import serializers
from drf.serializers import ModelSerializer
from utils.wechat import wechat


class UserCreateForms(ModelSerializer):
    code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['code', ]

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

    def create(self, validated_data):
        user_data = validated_data.pop('code', None)
        user, _ = User.objects.get_or_create(
            username=user_data["openid"], defaults={"password": make_password("123456")}
        )
        refresh = RefreshToken.for_user(user)
        return {"token": str(refresh.access_token)}


class SignInDateForms(ModelSerializer):
    class Meta:
        model = SignInDate
        fields = ["user", ]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def validate(self, attrs):
        user = self.context["request"].user
        if SignInDate.objects.filter(user=user, date=datetime.date.today()).exists():
            raise serializers.ValidationError("你今天已经签到了。")

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        amount = 1
        instance.user.balance += amount
        balance = instance.user.balance
        instance.user.save()
        AccountRecord.objects.create(
            user=instance.user,
            amount=amount,
            balance=balance,
            remark=f"签到获得{amount}积分",
        )
        return instance
