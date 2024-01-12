#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/12 15:57
# @file:content_detection.py
from alibabacloud_imm20200930.client import Client as imm20200930Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_imm20200930 import models as imm_20200930_models
from alibabacloud_tea_util import models as util_models
from django.conf import settings

from apps.draw.models import DrawHistory
from utils.redis import rd


class PornographicBloodTest:
    OSS_KEY = settings.ALIYUN_OSS_CONFIG.get("key", None)
    OSS_SECRET = settings.ALIYUN_OSS_CONFIG.get("secret", None)
    AUDIT_ENDPOINT = settings.ALIYUN_OSS_CONFIG.get("audit_endpoint", None)
    PROJECT_NAME = settings.ALIYUN_OSS_CONFIG.get("project_name", None)
    BUCKET = settings.ALIYUN_OSS_CONFIG.get("bucket", None)

    # @property
    def create_client(self) -> imm20200930Client:
        config = open_api_models.Config(
            access_key_id=self.OSS_KEY,
            access_key_secret=self.OSS_SECRET
        )
        # Endpoint 请参考 https://api.aliyun.com/product/imm
        config.endpoint = self.AUDIT_ENDPOINT
        return imm20200930Client(config)

    def initiate_request(self, image_name) -> str | None:
        client = self.create_client()
        create_image_moderation_task_request = imm_20200930_models.CreateImageModerationTaskRequest(
            project_name=self.PROJECT_NAME,
            source_uri=f'oss://{self.BUCKET}/{image_name}',
        )
        runtime = util_models.RuntimeOptions()
        res = client.create_image_moderation_task_with_options(create_image_moderation_task_request, runtime)
        return res.body.__dict__.get("task_id", None)

    def get_response(self, task_id):
        client = self.create_client()
        get_image_moderation_task_result = imm_20200930_models.GetImageModerationResultRequest(
            project_name=self.PROJECT_NAME,
            task_id=task_id,
            task_type='ImageModeration',
        )
        runtime = util_models.RuntimeOptions()
        try:
            res = client.get_image_moderation_result_with_options(get_image_moderation_task_result, runtime)
            print(res.body.__dict__.get("status", None))
            return res.body.__dict__.get("status", None), res.body.__dict__['moderation_result'].__dict__.get(
                "suggestion", None)
        except Exception as error:
            print(error)


audit = PornographicBloodTest()


def initiate_audit(image):
    try:
        result = audit.initiate_request(image.image.name.replace(settings.ALIYUN_OSS_CONFIG["host"], ""))
    except Exception as e:
        raise e
    if result:
        rd.hmset("audit_images", {image.id: result})
    else:
        raise Exception("Failed to initiate audit")


def get_audit_results():
    all_orders = rd.hgetall("audit_images")
    for id_, result in all_orders.items():
        status, suggestion = audit.get_response(result)
        if status == "Succeeded":
            rd.hdel("audit_images", id_)
            draw = DrawHistory.objects.get(id=id_)
            if suggestion == "block":
                txt = "图片违规，建议执行进一步操作（如直接删除或做限制处理）"
            elif suggestion == "review":
                txt = "图片疑似违规，建议人工复核"
            else:
                txt = "图片正常"
                draw.audit = True
            draw.audit_txt = f"审核结果为：{txt}"
            draw.save()
        elif status == "Failed":
            rd.hdel("audit_images", id_)
            draw = DrawHistory.objects.get(id=id_)
            draw.audit_txt = f"审核结果为：审核失败，建议人工复核"
            draw.save()
