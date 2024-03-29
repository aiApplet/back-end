from django.conf import settings
from django.db.models import Prefetch
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.draw import serializers, forms
from apps.draw.models import (
    DrawConfig,
    PromptAssistant,
    RandomPrompt,
    Styles,
    Loras,
    DrawHistory,
    UserLike,
    UserComment,
)
from core import exceptions
from core.exceptions import raise_business_exception
from drf import mixins
from drf import viewsets
from drf.pagination import PageNumberPagination
from drf.permissions import BalancePermission
from drf.response import success_response
from utils.aliyun import aliyun
from utils.content_detection import get_audit_results
from utils.redis import rd
from utils.utils import random_dict_from_list


# Create your views here.


class DrawViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = DrawConfig.objects.all()
    serializer_class = serializers.DrawHistoryImageSerializer
    create_form_class = forms.DrawConfigCreateForms
    permission_classes = [IsAuthenticated, BalancePermission]

    def create(self, request, *args, **kwargs):
        """
        lora 格式 [{"id": 1, "weight": 1}]
        """
        return super().create(request, *args, **kwargs)


class PromptsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = PromptAssistant.objects.all()
    serializer_class = serializers.PromptAssistantSerializer

    @method_decorator(cache_page(3600 * 24))  # 缓存1天
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RandomPromptViewSet(APIView):
    queryset = RandomPrompt.objects.all()

    def get(self, request, *args, **kwargs) -> dict:
        prompt = self.queryset.first()
        return success_response(data=random_dict_from_list(prompt.prompts))


class AliyunOssTokenViewSet(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        tags=["阿里云配置"],
        summary="获取阿里云配置，用于上传阿里云。需要参数secret_key，使用SHA256加密微信小程序appid",
        description="""
            {
                "accessid": "",
                "host": "",
                "policy": "",
                "signature": "",
                "expire": 1692871041.288708,
                "dir": "media/font_end/",
            }
            """,
    )
    def get(self, request, *args, **kwargs) -> dict:
        if settings.ALIYUN_OSS_ENABLE:
            token = aliyun.get_token()
            return success_response(token)
        raise_business_exception(exceptions.EXCEPTION_SERVER_NOT_ENABLE, app="draw")


class StylesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Styles.objects.all()
    serializer_class = serializers.StylesSerializer

    @method_decorator(cache_page(60 * 60))  # 缓存1小时
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class LorasViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Loras.objects.all()
    serializer_class = serializers.LorasSerializer

    @method_decorator(cache_page(60 * 60))  # 缓存1小时
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PicturesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = DrawHistory.objects.filter(audit=True)
    serializer_class = serializers.DrawHistorySerializer
    pagination_class = PageNumberPagination
    filterset_fields = ["config__style", "user"]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["create_time", "like_count", "comment_count"]  # 可以排序的字段
    ordering = ["-create_time"]  # 默认排序
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if settings.ENABLE_IMAGE_AUDIT:
            get_audit_results()
        return (
            super()
            .get_queryset()
            .select_related("config")
            .prefetch_related(Prefetch("config__style"))
            .select_related("user")
            .prefetch_related(
                Prefetch(
                    "history_set",
                    queryset=UserLike.objects.filter(user=self.request.user),
                )
            )
        )


class UserLikeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserLike.objects.all()
    serializer_class = serializers.UserLikeSerializer
    create_form_class = forms.UserLikeForm
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.save()

    @extend_schema(
        tags=["用户点赞"],
        summary="删除用户点赞对象",
        parameters=[
            OpenApiParameter("history", description="图片ID", required=True, type=str),
        ],
    )
    @action(methods=["delete"], detail=False)
    def delete(self, request, *args, **kwargs):
        history = request.data.get("history", "")
        if not history:
            raise_business_exception(exceptions.EXCEPTION_PARAMETER_FORMAT_ERROR)
        instance = (
            self.get_queryset().filter(user=self.request.user, history=history).first()
        )
        if not instance:
            raise_business_exception(exceptions.EXCEPTION_DATA_INCLUDE_INVALID_IDS)
        instance.delete()
        return success_response()


class UserCommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = UserComment.objects.all()
    serializer_class = serializers.UserCommentSerializer
    create_form_class = forms.UserCommentForm
    permission_classes = [IsAuthenticated]
    filterset_fields = [
        "history",
    ]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.save()
