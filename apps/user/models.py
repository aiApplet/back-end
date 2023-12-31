from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.conf import settings


# Create your models here.
class User(AbstractUser):
    avatar = models.CharField(max_length=100, default=settings.DEFAULT_AVATAR, verbose_name="头像")
    nickname = models.CharField(max_length=100, verbose_name="微信昵称")

    class Meta:
        db_table = "user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ["-id"]

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = f"游客{self.id}"
        super().save(*args, **kwargs)


class GroupProxy(Group):
    class Meta:
        proxy = True
        verbose_name = "角色"
        verbose_name_plural = verbose_name


class PermissionProxy(Permission):
    class Meta:
        proxy = True
        verbose_name = "权限"
        verbose_name_plural = verbose_name
