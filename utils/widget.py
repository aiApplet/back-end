#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/07 20:01
# @file:widget.py
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html


class CustomAdminFileWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        result = []
        if hasattr(value, "url"):
            result.append(
                f"""<a href="{value.url}" target="_blank">
                      <img 
                        src="{value.url}" alt="{value}" 
                        width="200" height="200"
                        style="object-fit: cover;"
                      />
                    </a>"""
            )
        result.append(super().render(name, value, attrs, renderer))
        return format_html("".join(result))
