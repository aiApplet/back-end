#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/05 22:14
# @file:forms.py
import base64
import json
from io import BytesIO

from django.core.files import File
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from apps.draw import const
from apps.draw.models import DrawConfig, DrawHistory, Loras, UserLike, UserComment
from apps.user.const import RewardTypeChoices
from apps.user.models import AccountRecord
from core import exceptions
from core.exceptions import raise_business_exception
from drf.serializers import ModelSerializer
from utils.aliyun import upload_image
from utils.content_detection import initiate_audit
from utils.stable_diffusion import StableDiffusion
from utils.utils import random_name


class DrawConfigCreateForms(ModelSerializer):
    lora = serializers.JSONField(required=False)

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
        }

    def validate_lora(self, value):
        data = {}
        if value:
            if not isinstance(value, list):
                raise_business_exception(exceptions.EXCEPTION_PARAMETER_FORMAT_ERROR, "lora参数必须为数组")
            for item in value:
                if not isinstance(item, dict):
                    raise_business_exception(exceptions.EXCEPTION_PARAMETER_FORMAT_ERROR, "lora参数必须为字典")
                if "id" not in item or "weight" not in item:
                    raise_business_exception(exceptions.EXCEPTION_PARAMETER_FORMAT_ERROR, "lora参数必须包含path和weight字段")
                else:
                    if not isinstance(item["id"], int) or not isinstance(item["weight"], int):
                        raise_business_exception(exceptions.EXCEPTION_PARAMETER_FORMAT_ERROR, "lora参数的path和weight字段必须为整数")
                    else:
                        lora = Loras.objects.filter(id=item["id"]).first()
                        if not lora:
                            raise_business_exception(exceptions.EXCEPTION_PARAMETER_FORMAT_ERROR, "找不到lora")
                        else:
                            data[lora.nickname] = item["weight"]
        return data

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["sampler_name"] = settings.STABLE_DIFFUSION_CONFIG[
            "sampler_name"
        ]
        loras = validated_data.get("lora", None)
        lora_prompt = ""
        if loras:
            for lora, weight in loras.items():
                lora_prompt += f"<lora:{lora}:{weight}>,"

        prompt = f"{lora_prompt}{validated_data['style'].style}{validated_data['prompt']}{'' if validated_data['prompt'][-1] == ',' else ','}"
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
            "/sdapi/v1/txt2img", instance, user
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
            user=user,
            image=img_file,
            status=status,
        )
        if settings.ENABLE_IMAGE_AUDIT:
            initiate_audit(draw)
        seed = json.loads(result["info"])["seed"]
        instance.seed = seed
        instance.save()
        if not user.is_superuser:
            user.balance -= 1
            user.save()
            AccountRecord.objects.create(
                user=user,
                amount=settings.GEN_IMAGE_COST,
                balance=user.balance,
                record_type=False,
                reward_type=RewardTypeChoices.DRAW.value,
                remark=f"使用AI绘图，扣除积分:{settings.GEN_IMAGE_COST}",
            )
        return draw


class UserLikeForm(ModelSerializer):
    class Meta:
        model = UserLike
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": False},
        }

    def validate(self, attrs):
        if UserLike.objects.filter(
                user=self.context["request"].user,
                history=attrs["history"],
                create_time__date=timezone.now().date(),
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
                    user=self.context["request"].user, history=attrs["history"]
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
