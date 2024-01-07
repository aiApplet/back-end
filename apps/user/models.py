from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.conf import settings

from apps.user import const
from utils.aliyun import upload_image


# Create your models here.
class User(AbstractUser):
    avatar = models.CharField(
        max_length=100, default=settings.DEFAULT_AVATAR, verbose_name="头像"
    )
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
    record_type = models.BooleanField(
        default=True, verbose_name="记录类型", choices=((True, "收入"), (False, "支出"))
    )
    reward_type = models.PositiveSmallIntegerField(
        verbose_name="收支分类", choices=const.RewardTypeChoices.choices
    )
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


class RechargeableCard(models.Model):
    card_number = models.CharField(max_length=20, unique=True, verbose_name="卡号")
    amount = models.PositiveIntegerField(default=0, verbose_name="金额")
    is_used = models.BooleanField(default=False, verbose_name="是否已使用")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    use_time = models.DateTimeField(null=True, blank=True, verbose_name="使用时间")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="用户",
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        db_table = "rechargeable_card"
        verbose_name = "充值卡"
        verbose_name_plural = verbose_name


class CarouselFigure(models.Model):
    image = models.ImageField(upload_to="carousel/", verbose_name="图片")
    link = models.CharField(max_length=255, verbose_name="链接")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    sort = models.PositiveSmallIntegerField(default=0, verbose_name="排序")
    is_show = models.BooleanField(default=True, verbose_name="是否显示")

    class Meta:
        db_table = "carousel_figure"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name
        ordering = ["-sort", "-id"]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.image = upload_image(
            f"media/carousel/{self.image.name}", self.image.read()
        )
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
