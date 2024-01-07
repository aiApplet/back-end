from django.contrib import admin
from django.db.models import ImageField
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.draw.models import (
    Styles,
    Loras,
    DrawConfig,
    DrawHistory,
    PromptAssistant,
    RandomPrompt,
)
from utils.widget import CustomAdminFileWidget


# Register your models here.


class StylesAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "style",
        "sort",
    ]
    list_editable = [
        "sort",
    ]


class LorasAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "nickname", "weight", "cover_img", "sort"]
    list_editable = [
        "sort",
    ]
    formfield_overrides = {ImageField: {"widget": CustomAdminFileWidget}}

    def cover_img(self, obj):
        return format_html(
            '<img src="{}" style="max-width:200px; max-height:200px"/>'.format(
                obj.cover
            )
        )

    cover_img.short_description = "封面图"


class DrawConfigAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "prompt",
        "negative_prompt",
        "width",
        "height",
        "seed",
        "sampler_name",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DrawHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "front_cover_img_data"]
    list_per_page = 10

    def front_cover_img_data(self, obj):
        html = ""
        if obj.image:
            html = f"""
              <div style="position: relative">
                <a href="{obj.image}" target="_blank">
                  <img src="{obj.image}" width="100%" height="100%"> 
                </a>
                <div style="position: absolute; top: 0; left: 0; display: none;" class="zoom-img">
                  <img src="{obj.image}">
                  <div 
                    style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; cursor: zoom-out;" 
                    onclick="this.parentElement.style.display='none'">
                  </div>
                </div>
              </div>
            """

        return mark_safe(html)

    front_cover_img_data.short_description = "图片"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PromptAssistantAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]


class RandomPromptAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]


admin.site.register(Styles, StylesAdmin)
admin.site.register(Loras, LorasAdmin)
admin.site.register(DrawConfig, DrawConfigAdmin)
admin.site.register(DrawHistory, DrawHistoryAdmin)
admin.site.register(PromptAssistant, PromptAssistantAdmin)
# admin.site.register(RandomPrompt, RandomPromptAdmin)
