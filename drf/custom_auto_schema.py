#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/02 16:00
# @file:CustomAutoSchema.py
from typing import List, Optional

from rest_framework.views import APIView
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_serializer_context, get_doc
from rest_framework.generics import GenericAPIView
from drf_spectacular.drainage import error


class CustomAutoSchema(AutoSchema):
    def get_request_serializer(self):
        """重写此方法用于使用自定义的 request serializer"""

        view = self.view
        context = build_serializer_context(view)
        try:
            if isinstance(view, GenericAPIView):
                if view.__class__.get_serializer == GenericAPIView.get_serializer:
                    action = self.method_mapping[self.method.lower()]
                    form_class = getattr(view, f"{action}_form_class", None)
                    if not form_class:
                        form_class = view.get_serializer_class()
                    return form_class(context=context)
                return view.get_serializer(context=context)
            elif isinstance(view, APIView):
                if callable(getattr(view, "get_serializer", None)):
                    return view.get_serializer(context=context)
                elif callable(getattr(view, "get_serializer_class", None)):
                    return view.get_serializer_class()(context=context)
                elif hasattr(view, "serializer_class"):
                    return view.serializer_class
                else:
                    error(
                        "unable to guess serializer. This is graceful fallback handling for APIViews. "
                        "Consider using GenericAPIView as view base class, if view is under your control. "
                        "Either way you may want to add a serializer_class (or method). Ignoring view for now."
                    )
            else:
                error(
                    "Encountered unknown view base class. Please report this issue. Ignoring for now"
                )
        except Exception as exc:
            error(
                f"exception raised while getting serializer. Hint: "
                f"Is get_serializer_class() returning None or is get_queryset() not working without "
                f"a request? Ignoring the view for now. (Exception: {exc})"
            )

    def get_tags(self) -> List[str]:
        """重写此方法适用于根据模型定义接口分类"""
        return [self.get_model_verbose_name()]

    def get_model_verbose_name(self):
        # 获取与视图集关联的模型
        model = self.view.queryset.model
        # 返回模型的verbose_name
        return model._meta.verbose_name

    def get_summary(self) -> Optional[str]:
        """override this for custom behaviour"""
        model = self.get_model_verbose_name()
        if self.method.lower() == "get":
            text = f"获取{model}列表"
        elif self.method.lower() == "post":
            text = f"创建{model}对象"
        elif self.method.lower() == "put":
            text = f"全量修改{model}对象"
        elif self.method.lower() == "patch":
            text = f"部分修改{model}对象"
        elif self.method.lower() == "delete":
            text = f"删除{model}对象"
        else:
            text = f"{model}"
        return text

    def get_description(self) -> str:  # type: ignore[override]
        """override this for custom behaviour"""
        text = self.get_summary()
        action_or_method = getattr(
            self.view, getattr(self.view, "action", self.method.lower()), None
        )
        action_doc = get_doc(action_or_method)
        return action_doc or text
