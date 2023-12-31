#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/01 00:12
# @file:forms.py
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User
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

