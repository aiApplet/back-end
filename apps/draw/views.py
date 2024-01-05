from django.shortcuts import render

from apps.draw.models import DrawConfig
from drf import mixins
from drf import viewsets


# Create your views here.

class DrawViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = DrawConfig.objects.all()
