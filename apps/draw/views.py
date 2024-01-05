from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.draw import serializers, forms
from apps.draw.models import DrawConfig, PromptAssistant, RandomPrompt, Styles, Loras, DrawHistory, UserLike, \
    UserComment
from drf import mixins
from drf import viewsets
from drf.pagination import PageNumberPagination
from drf.response import success_response
from utils.utils import random_dict_from_list


# Create your views here.

class DrawViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = DrawConfig.objects.all()
    serializer_class = serializers.DrawHistoryImageSerializer
    create_form_class = forms.DrawConfigCreateForms
    permission_classes = [IsAuthenticated, ]


class PromptsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = PromptAssistant.objects.all()
    serializer_class = serializers.PromptAssistantSerializer


class RandomPromptViewSet(APIView):
    queryset = RandomPrompt.objects.all()

    def get(self, request, *args, **kwargs) -> dict:
        prompt = self.queryset.first()
        return success_response(data=random_dict_from_list(prompt.prompts))


class StylesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Styles.objects.all()
    serializer_class = serializers.StylesSerializer


class LorasViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Loras.objects.all()
    serializer_class = serializers.LorasSerializer


class PicturesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = DrawHistory.objects.all()
    serializer_class = serializers.DrawHistorySerializer
    pagination_class = PageNumberPagination
    filterset_fields = ["config__style", ]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['create_time', 'like_count', 'comment_count']  # 可以排序的字段
    ordering = ['-create_time']  # 默认排序


class UserLikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserLike.objects.all()
    serializer_class = serializers.UserLikeSerializer
    create_form_class = forms.UserLikeForm
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserCommentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserComment.objects.all()
    serializer_class = serializers.UserCommentSerializer
    create_form_class = forms.UserCommentForm
    permission_classes = [IsAuthenticated]
    filterset_fields = ["history", ]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
