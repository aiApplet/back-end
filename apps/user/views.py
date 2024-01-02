from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from apps.user import serializers, forms
from apps.user.models import User
from drf import mixins
from drf import viewsets
from drf.response import success_response


# Create your views here.


class UserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    create_form_class = forms.UserCreateForms

    def get_permissions(self):
        """
        实例化和返回此视图所需的权限列表。
        """
        if self.action == 'create':
            # 如果是 create 操作，则不需要特定权限
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """获取头像、id、昵称"""
        serializer = self.get_serializer(self.request.user)
        return success_response(serializer.data)

    def create(self, request, *args, **kwargs):
        """拿到微信code查询或者创建一个用户，返回token"""
        form_class = getattr(self, "create_form_class", None)
        serializer = form_class(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return success_response(instance)
