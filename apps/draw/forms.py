#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/05 22:14
# @file:forms.py
import base64
from io import BytesIO

from django.core.files import File
from django.db import transaction

from apps.draw import const
from apps.draw.models import DrawConfig, DrawHistory
from core import exceptions
from core.exceptions import raise_business_exception
from drf.serializers import ModelSerializer
from utils.stable_diffusion import StableDiffusion
from utils.utils import random_name


class DrawConfigCreateForms(ModelSerializer):
    class Meta:
        model = DrawConfig
        exclude = ["id", "config"]
        extra_kwargs = {
            "negative_prompt": {"required": False, },
            "seed": {"required": False, },
            "sampler_name": {"required": False, "default": "LCM"},
            "lora": {"required": False, },
        }

    @transaction.atomic
    def create(self, validated_data):
        prompt = f"{validated_data['prompt']}{'' if validated_data['prompt'][-1] == ',' else ','}<lora:LCM:1>,"
        validated_data["config"] = {
            "prompt": prompt,
            "negative_prompt": validated_data['negative_prompt'],
            "seed": validated_data['seed'] or -1,
            "sampler_name": "LCM",
            "cfg_scale": 2,
            "height": validated_data['height'],
            "width": validated_data['width'],
            "steps": 8,
            "alwayson_scripts": {},
            "override_settings": {
                "sd_vae": "Automatic",
                "sd_model_checkpoint": "RealitiesEdgeXLLCM_TURBOXL.safetensors [c1d5646e8f]"
            }
        }
        instance = super().create(validated_data)
        result = StableDiffusion.generate_image("http://172.24.42.191:7860/sdapi/v1/txt2img", instance.config)
        images = result.get("images", None)
        if not images:
            raise_business_exception(exceptions.EXCEPTION_BUILD_FAILED_ERROR, "生成失败", result, "draw")
        base64_data = base64.b64decode(images[0])
        img_io = BytesIO(base64_data)
        image_name = f"{random_name()}.png"
        img_file = File(img_io, name=image_name)
        status = const.DrawHistoryStatusChoices.SUCCESS.value
        draw = DrawHistory.objects.create(config=instance, user=self.context["request"].user, image=img_file, status=status)
        return draw
