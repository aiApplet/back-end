from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin

from apps.user.models import GroupProxy, User, PermissionProxy


# 定义一个新的UserAdmin
class UserAdmin(BaseUserAdmin):
    # 定义admin面板中显示的字段
    list_display = ("username", "email", "nickname", "is_staff")
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
