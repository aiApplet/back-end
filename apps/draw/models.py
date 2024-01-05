import os

from django.db import models

from apps.draw import const
from apps.user.models import User


# Create your models here.

class Styles(models.Model):
    name = models.CharField(max_length=255, default="", verbose_name="风格名称")
    style = models.CharField(default="", max_length=255, verbose_name="风格")
    sort = models.PositiveSmallIntegerField(
        default=0, verbose_name="排序", help_text="排序"
    )

    class Meta:
        verbose_name = "风格"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name


class Loras(models.Model):
    name = models.CharField(max_length=100, default="", verbose_name="Lora中文昵称")
    nickname = models.CharField(max_length=100, default="", verbose_name="Lora名称")
    weight = models.FloatField(default=1, verbose_name="权重")
    cover = models.ImageField(upload_to='lora/', default='', verbose_name='封面')
    sort = models.PositiveSmallIntegerField(
        default=0, verbose_name="排序", help_text="排序"
    )

    class Meta:
        verbose_name = "Lora模型"
        verbose_name_plural = verbose_name
        ordering = ['-sort', '-id']

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # 获取图片路径
        filepath = self.cover.path

        # 判断文件是否存在
        if os.path.exists(filepath):
            # 删除文件
            os.remove(filepath)

        super().delete(*args, **kwargs)


class DrawConfig(models.Model):
    prompt = models.CharField(max_length=255, default="", verbose_name="提示词")
    negative_prompt = models.CharField(max_length=255, default="", verbose_name="负面提示词")
    config = models.JSONField(default=dict, verbose_name="配置")
    width = models.PositiveSmallIntegerField(verbose_name="宽度")
    height = models.PositiveSmallIntegerField(verbose_name="高度")
    seed = models.SmallIntegerField(default=-1, verbose_name="种子")
    sampler_name = models.CharField(default="", max_length=100, verbose_name="采样器")
    lora = models.ManyToManyField(Loras, blank=True, verbose_name="Lora模型")

    class Meta:
        verbose_name = "绘图配置"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.prompt


class DrawHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    config = models.ForeignKey(DrawConfig, on_delete=models.CASCADE, verbose_name="配置")
    image = models.ImageField(upload_to='draw/', verbose_name='图片')
    status = models.PositiveSmallIntegerField(choices=const.DrawHistoryStatusChoices.choices,
                                              default=const.DrawHistoryStatusChoices.IN_WORK.value, verbose_name="状态")

    class Meta:
        verbose_name = "绘图历史"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}"


class PromptAssistant(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    prompts = models.JSONField(default=dict, verbose_name="提示词")

    class Meta:
        verbose_name = "提示词助手"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name


class RandomPrompt(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    prompts = models.JSONField(default=dict, verbose_name="提示词")

    class Meta:
        verbose_name = "随机提示词"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name
