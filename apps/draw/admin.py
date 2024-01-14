from django.conf import settings
from django.contrib import admin
from django.db.models import ImageField
from django.db.models.signals import pre_delete
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.draw.models import (
    Styles,
    Loras,
    DrawConfig,
    DrawHistory,
    PromptAssistant, Machines, MachineLogs,
)
from utils.aliyun import delete_image
from utils.redis import rd
from utils.widget import CustomAdminFileWidget


# Register your models here.

class MachinesAdmin(admin.ModelAdmin):
    list_display = ["name", "agreement", "ip", "post", "enabled"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change and (obj.enabled is False):
            rd.delete(obj.id)
        else:
            check_machine()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        rd.delete(obj.id)


class MachineLogsAdmin(admin.ModelAdmin):
    list_display = ["machine", "user", "create_time", "total_time", "remark"]


def check_machine():
    machine_ids = Machines.objects.filter(enabled=True).values_list("id", flat=True)
    for machine_id in machine_ids:
        status = rd.get(machine_id)
        if status is None:
            rd.set(machine_id, 0)


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

    def delete_queryset(self, request, queryset):
        """Since django's default batch deletion does not trigger the model's delete method and signal, we need to redo this method."""
        for query in queryset:
            delete_image(
                query.cover.name.replace(settings.ALIYUN_OSS_CONFIG["host"], "")
            )
        pre_delete.send(sender=queryset[0].__class__, instance=queryset[0])
        queryset.delete()


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
    list_display = ["user", "audit", "audit_txt", "front_cover_img_data", "create_time", "like_count", "comment_count"]
    list_per_page = 10
    list_editable = ["audit", ]

    def front_cover_img_data(self, obj):
        html = ""
        if obj.image:
            html = f"""
              <div style="position: relative">
                <a href="{obj.image}" target="_blank">
                  <img src="{obj.image}" width="50%" height="50%"> 
                </a>
              </div>
            """

        return mark_safe(html)

    front_cover_img_data.short_description = "图片"

    def has_add_permission(self, request):
        return False

    def delete_queryset(self, request, queryset):
        """Since django's default batch deletion does not trigger the model's delete method and signal, we need to redo this method."""
        for query in queryset:
            delete_image(
                query.image.name.replace(settings.ALIYUN_OSS_CONFIG["host"], "")
            )
        pre_delete.send(sender=queryset[0].__class__, instance=queryset[0])
        queryset.delete()


class PromptAssistantAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]


admin.site.register(Machines, MachinesAdmin)
admin.site.register(MachineLogs, MachineLogsAdmin)
admin.site.register(Styles, StylesAdmin)
admin.site.register(Loras, LorasAdmin)
admin.site.register(DrawConfig, DrawConfigAdmin)
admin.site.register(DrawHistory, DrawHistoryAdmin)
admin.site.register(PromptAssistant, PromptAssistantAdmin)
