from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin

from apps.user.models import GroupProxy, User, PermissionProxy, AccountRecord, SignInDate, RechargeableCard


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
    list_display = ['name', 'codename']  # or any other fields you wish to display
    fields = ['name', 'codename', 'content_type']  # Detail view configuration
    search_fields = ['name', 'codename']  # Optional: to add a search box


# Register the admin class with the associated model
# 注册您的User模型和UserAdmin
admin.site.register(User, UserAdmin)

admin.site.register(PermissionProxy, PermissionAdmin)
admin.site.register(GroupProxy, GroupAdmin)

from django.contrib.auth.models import Group

admin.site.unregister(Group)


class AccountRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'balance', 'create_time', 'record_type', 'reward_type', 'remark', ]
    search_fields = ['user__id', 'user__nickname']
    list_filter = ['create_time', 'record_type', 'reward_type']
    readonly_fields = ['user']


admin.site.register(AccountRecord, AccountRecordAdmin)


class SignInDateAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']
    search_fields = ['user__id', 'user__nickname']
    list_filter = ['date', ]
    readonly_fields = ['user']


admin.site.register(SignInDate, SignInDateAdmin)


class RechargeableCardAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'amount', 'is_used', 'create_time', 'use_time', 'user']
    search_fields = ['card_number', 'user__nickname', 'user__nickname']
    list_filter = ['create_time', 'is_used', 'amount']
    readonly_fields = ['user']


admin.site.register(RechargeableCard, RechargeableCardAdmin)
