#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/08 02:04
# @file:signals.py
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.http import HttpRequest
from django.urls import reverse
from django.utils.cache import _generate_cache_header_key

from apps.user.models import CarouselFigure


@receiver(post_save, sender=CarouselFigure)
@receiver(post_delete, sender=CarouselFigure)
def clear_carousel_figure_cache(sender, **kwargs):
    path = reverse("user:carousel_figure-list")
    request = HttpRequest()
    request.path = path
    request.META["HTTP_HOST"] = settings.LOCAL_HOST
    key = _generate_cache_header_key("", request)
    cache.delete(key)
