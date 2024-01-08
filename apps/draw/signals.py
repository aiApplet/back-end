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

from apps.draw.models import Styles, Loras, PromptAssistant


@receiver(post_save, sender=Styles)
@receiver(post_delete, sender=Styles)
def clear_styles_cache(sender, **kwargs):
    path = reverse('draw:styles-list')
    request = HttpRequest()
    request.path = path
    request.META['HTTP_HOST'] = settings.LOCAL_HOST
    key = _generate_cache_header_key("", request)
    cache.delete(key)


@receiver(post_save, sender=Loras)
@receiver(post_delete, sender=Loras)
def clear_loras_cache(sender, **kwargs):
    path = reverse('draw:loras-list')
    request = HttpRequest()
    request.path = path
    request.META['HTTP_HOST'] = settings.LOCAL_HOST
    key = _generate_cache_header_key("", request)
    cache.delete(key)


@receiver(post_save, sender=PromptAssistant)
@receiver(post_delete, sender=PromptAssistant)
def clear_prompts_cache(sender, **kwargs):
    path = reverse('draw:prompts-list')
    request = HttpRequest()
    request.path = path
    request.META['HTTP_HOST'] = settings.LOCAL_HOST
    key = _generate_cache_header_key("", request)
    cache.delete(key)
