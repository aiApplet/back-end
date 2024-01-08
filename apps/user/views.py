from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.user import serializers, forms
from apps.user.models import (
    User,
    SignInDate,
    AccountRecord,
    RechargeableCard,
    CarouselFigure,
)
from drf import mixins
from drf import viewsets
from drf.pagination import PageNumberPagination
from drf.response import success_response


# Create your views here.


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    create_form_class = forms.UserCreateForms

    def get_permissions(self):
        """
        实例化和返回此视图所需的权限列表。
        """
        if self.action in ["create", "sign_in"]:
            # 如果是 create 操作，则不需要特定权限
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """获取头像、id、昵称、积分"""
        serializer = self.get_serializer(self.request.user)
        return success_response(serializer.data)

    def create(self, request, *args, **kwargs):
        """拿到微信code查询或者创建一个用户，返回token。parent_id父ID，非必填，邀请分享人，用于奖励。"""
        form_class = getattr(self, "create_form_class", None)
        serializer = form_class(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return success_response(instance)

    @action(methods=["post"], detail=False)
    def sign_in(self, request, *args, **kwargs):
        """登录（测试用）"""
        from rest_framework_simplejwt.tokens import RefreshToken

        user = User.objects.first()
        refresh = RefreshToken.for_user(user)
        return success_response({"token": str(refresh.access_token)})


class SignInViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = SignInDate.objects.all()
    serializer_class = forms.SignInDateForms
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AccountRecordViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = AccountRecord.objects.all()
    serializer_class = serializers.AccountRecordSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    pagination_class = PageNumberPagination
    filterset_fields = ["record_type", "reward_type"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class RechargeableCardViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = RechargeableCard.objects.filter(is_used=False)
    create_form_class = forms.RechargeableCardForms
    serializer_class = serializers.RechargeableCardSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.action == "list":
            return super().get_queryset().filter(user=self.request.user)
        return super().get_queryset()


class CarouselFigureViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CarouselFigure.objects.filter(is_show=True)
    serializer_class = serializers.CarouselFigureSerializer

    @method_decorator(cache_page(3600 * 24))  # 缓存24小时
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
