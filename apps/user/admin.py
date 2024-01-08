from django.conf import settings
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from django.db.models import ImageField
from django.db.models.signals import pre_delete
from django.utils.html import format_html

from apps.user.models import (
    GroupProxy,
    User,
    PermissionProxy,
    AccountRecord,
    SignInDate,
    RechargeableCard,
    CarouselFigure,
)
from utils.aliyun import delete_image
from utils.widget import CustomAdminFileWidget


# 定义一个新的UserAdmin
class UserAdmin(BaseUserAdmin):
    # 定义admin面板中显示的字段
    list_display = ("username", "email", "nickname", "balance", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "个人信息",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "nickname",
                    "avatar",
                )
            },
        ),
        (
            "权限",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("重要日期", {"fields": ("last_login", "date_joined")}),
    )


# Define the admin class
class PermissionAdmin(admin.ModelAdmin):
    list_display = ["name", "codename"]  # or any other fields you wish to display
    fields = ["name", "codename", "content_type"]  # Detail view configuration
    search_fields = ["name", "codename"]  # Optional: to add a search box


# Register the admin class with the associated model
# 注册您的User模型和UserAdmin
admin.site.register(User, UserAdmin)

admin.site.register(PermissionProxy, PermissionAdmin)
admin.site.register(GroupProxy, GroupAdmin)

from django.contrib.auth.models import Group

admin.site.unregister(Group)


class AccountRecordAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "amount",
        "balance",
        "create_time",
        "record_type",
        "reward_type",
        "remark",
    ]
    search_fields = ["user__id", "user__nickname"]
    list_filter = ["create_time", "record_type", "reward_type"]
    readonly_fields = ["user"]


admin.site.register(AccountRecord, AccountRecordAdmin)


class SignInDateAdmin(admin.ModelAdmin):
    list_display = ["user", "date"]
    search_fields = ["user__id", "user__nickname"]
    list_filter = [
        "date",
    ]
    readonly_fields = ["user"]


admin.site.register(SignInDate, SignInDateAdmin)


class RechargeableCardAdmin(admin.ModelAdmin):
    list_display = [
        "card_number",
        "amount",
        "is_used",
        "create_time",
        "use_time",
        "user",
    ]
    search_fields = ["card_number", "user__nickname", "user__nickname"]
    list_filter = ["create_time", "is_used", "amount"]
    readonly_fields = ["user"]


admin.site.register(RechargeableCard, RechargeableCardAdmin)


class CarouselFigureAdmin(admin.ModelAdmin):
    list_display = ["id", "link", "image_img", "create_time", "sort", "is_show"]
    search_fields = [
        "link",
    ]
    list_filter = ["create_time", "is_show"]
    list_editable = ["is_show", "sort"]
    formfield_overrides = {ImageField: {"widget": CustomAdminFileWidget}}  # Here

    def image_img(self, obj):
        return format_html(
            '<img src="{}" style="max-width:200px; max-height:200px"/>'.format(
                obj.image
            )
        )

    image_img.short_description = "图片"

    def delete_queryset(self, request, queryset):
        """Since django's default batch deletion does not trigger the model's delete method and signal, we need to redo this method."""
        for query in queryset:
            delete_image(query.image.name.replace(settings.ALIYUN_OSS_CONFIG["host"], ''))
        pre_delete.send(sender=queryset[0].__class__, instance=queryset[0])
        queryset.delete()


admin.site.register(CarouselFigure, CarouselFigureAdmin)
