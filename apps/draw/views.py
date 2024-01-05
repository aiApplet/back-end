from django.shortcuts import render
from rest_framework.views import APIView

from apps.draw import serializers, forms
from apps.draw.models import DrawConfig, PromptAssistant, RandomPrompt, Styles, Loras
from drf import mixins
from drf import viewsets
from drf.response import success_response
from utils.utils import random_dict_from_list


# Create your views here.

class DrawViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = DrawConfig.objects.all()
    serializer_class = serializers.DrawHistorySerializer
    create_form_class = forms.DrawConfigCreateForms


class PromptsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = PromptAssistant.objects.all()
    serializer_class = serializers.PromptAssistantSerializer


class RandomPromptViewSet(APIView):
    queryset = RandomPrompt.objects.all()

    def get(self, request, *args, **kwargs) -> dict:
        prompt = self.queryset.first()
        return success_response(data=random_dict_from_list(prompt.prompts))


class StylesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Styles.objects.all()
    serializer_class = serializers.StylesSerializer


class LorasViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Loras.objects.all()
    serializer_class = serializers.LorasSerializer
