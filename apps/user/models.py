from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.conf import settings


# Create your models here.
class User(AbstractUser):
    avatar = models.CharField(max_length=100, default=settings.DEFAULT_AVATAR, verbose_name="头像")
    nickname = models.CharField(max_length=100, verbose_name="微信昵称")
    balance = models.PositiveIntegerField(default=0, verbose_name="余额")

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


class AccountRecord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    amount = models.PositiveIntegerField(default=0, verbose_name="金额")
    balance = models.PositiveIntegerField(verbose_name="余额")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    account_type = models.BooleanField(default=True, verbose_name="账户类型", choices=((True, "收入"), (False, "支出")))
    remark = models.CharField(max_length=255, null=True, blank=True, verbose_name="备注")

    class Meta:
        db_table = "account_record"
        verbose_name = "账户记录"
        verbose_name_plural = verbose_name
        ordering = ["-id"]


class SignInDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    date = models.DateField(auto_now_add=True, verbose_name="日期")

    class Meta:
        db_table = "sign_in_date"
        verbose_name = "签到日期"
        verbose_name_plural = verbose_name
        ordering = ["-id"]
