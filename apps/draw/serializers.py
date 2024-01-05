#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/05 21:51
# @file:serializers.py
from apps.draw.models import PromptAssistant, DrawConfig, Styles, Loras, DrawHistory
from drf.serializers import ModelSerializer


class DrawHistorySerializer(ModelSerializer):
    class Meta:
        model = DrawHistory
        fields = ('image',)


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