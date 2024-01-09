#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/05 22:14
# @file:forms.py
import base64
import json
from datetime import datetime
from io import BytesIO

from django.core.files import File
from django.db import transaction
from django.conf import settings
from rest_framework import serializers

from apps.draw import const
from apps.draw.models import DrawConfig, DrawHistory, UserLike, UserComment
from core import exceptions
from core.exceptions import raise_business_exception
from drf.serializers import ModelSerializer
from utils.aliyun import upload_image
from utils.stable_diffusion import StableDiffusion
from utils.utils import random_name


class DrawConfigCreateForms(ModelSerializer):
    class Meta:
        model = DrawConfig
        exclude = ["id", "config", "sampler_name"]
        extra_kwargs = {
            "negative_prompt": {
                "required": False,
                "default": settings.STABLE_DIFFUSION_CONFIG["negative_prompt"],
            },
            "seed": {
                "required": False,
                "default": settings.STABLE_DIFFUSION_CONFIG["seed"],
            },
            "lora": {
                "required": False,
            },
        }

    @transaction.atomic
    def create(self, validated_data):
        validated_data["sampler_name"] = settings.STABLE_DIFFUSION_CONFIG[
            "sampler_name"
        ]
        loras = validated_data.get("lora", None)
        lora_prompt = ""
        if loras:
            for lora in loras:
                lora_prompt += f"<lora:{lora.nickname}:{lora.weight}>,"
        prompt = f"{lora_prompt}{validated_data['style'].style}{validated_data['prompt']}{'' if validated_data['prompt'][-1] == ',' else ','}<lora:LCM:1>,"
        validated_data["config"] = {
            "prompt": prompt,
            "negative_prompt": validated_data["negative_prompt"],
            "seed": validated_data["seed"],
            "sampler_name": validated_data["sampler_name"],
            "cfg_scale": settings.STABLE_DIFFUSION_CONFIG["cfg_scale"],
            "height": validated_data["height"],
            "width": validated_data["width"],
            "steps": settings.STABLE_DIFFUSION_CONFIG["steps"],
            "alwayson_scripts": {},
            "override_settings": {
                "sd_vae": settings.STABLE_DIFFUSION_CONFIG["sd_vae"],
                "sd_model_checkpoint": settings.STABLE_DIFFUSION_CONFIG[
                    "sd_model_checkpoint"
                ],
            },
        }
        instance = super().create(validated_data)
        result = StableDiffusion.generate_image(
            "http://172.24.42.191:7860/sdapi/v1/txt2img", instance.config
        )
        images = result.get("images", None)
        if not images:
            raise_business_exception(
                exceptions.EXCEPTION_BUILD_FAILED_ERROR, "生成失败", result, "draw"
            )
        image_name = f"{random_name()}.png"
        base64_data = base64.b64decode(images[0])

        if settings.ALIYUN_OSS_ENABLE:
            img_file = upload_image(f"media/draw/{image_name}", base64_data)
        else:
            img_io = BytesIO(base64_data)
            img_file = File(img_io, name=image_name)
        status = const.DrawHistoryStatusChoices.SUCCESS.value
        draw = DrawHistory.objects.create(
            config=instance,
            user=self.context["request"].user,
            image=img_file,
            status=status,
        )
        seed = json.loads(result["info"])["seed"]
        instance.seed = seed
        instance.save()
        return draw


class UserLikeForm(ModelSerializer):
    class Meta:
        model = UserLike
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": False},
        }

    def validate(self, attrs):
        now = datetime.now()
        if UserLike.objects.filter(
            user=self.context["request"].user,
            draw_history=attrs["draw_history"],
            create_time__day=now.today(),
        ).exists():
            raise serializers.ValidationError("今日已经点过赞了，请明天再来。")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.history.like_count += 1
        instance.history.save()
        return instance


class UserCommentForm(ModelSerializer):
    class Meta:
        model = UserComment
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": False},
        }

    def validate(self, attrs):
        if (
            UserComment.objects.filter(
                user=self.context["request"].user, draw_history=attrs["draw_history"]
            ).count()
            > 5
        ):
            raise serializers.ValidationError("您今天已经评论过5次了，禁止再评论。")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.history.comment_count += 1
        instance.history.save()
        return instance
