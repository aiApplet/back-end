from django.contrib import admin
from django.utils.html import format_html

from apps.draw.models import Styles, Loras, DrawConfig, DrawHistory, PromptAssistant, RandomPrompt


# Register your models here.


class StylesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'style', 'sort', ]
    list_editable = ['sort', ]


class LorasAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'nickname', 'weight', 'cover_img', 'sort']
    list_editable = ['sort', ]

    def cover_img(self, obj):
        return format_html(
            '<img src="{}" style="max-width:200px; max-height:200px"/>'.format(
                obj.cover.url
            )
        )

    cover_img.short_description = "封面图"


class DrawConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'prompt', 'negative_prompt', 'width', 'height', 'seed', 'sampler_name']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DrawHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'image']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PromptAssistantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]


class RandomPromptAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]


admin.site.register(Styles, StylesAdmin)
admin.site.register(Loras, LorasAdmin)
admin.site.register(DrawConfig, DrawConfigAdmin)
admin.site.register(DrawHistory, DrawHistoryAdmin)
admin.site.register(PromptAssistant, PromptAssistantAdmin)
# admin.site.register(RandomPrompt, RandomPromptAdmin)
