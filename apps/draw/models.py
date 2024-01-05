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
        ordering = ['-sort', '-id']

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


class DrawConfig(models.Model):
    prompt = models.CharField(max_length=1000, default="", verbose_name="提示词")
    negative_prompt = models.CharField(max_length=255, default="", verbose_name="负面提示词")
    config = models.JSONField(default=dict, verbose_name="配置")
    width = models.PositiveSmallIntegerField(verbose_name="宽度")
    height = models.PositiveSmallIntegerField(verbose_name="高度")
    seed = models.CharField(max_length=100, default='-1', verbose_name="种子")
    sampler_name = models.CharField(default="", max_length=100, verbose_name="采样器")
    style = models.ForeignKey(Styles, on_delete=models.PROTECT, verbose_name="风格")
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
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    like_count = models.PositiveIntegerField(default=0, verbose_name="点赞数")
    comment_count = models.PositiveIntegerField(default=0, verbose_name="评论数")

    class Meta:
        verbose_name = "绘图历史"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}"


class UserLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    history = models.ForeignKey(DrawHistory, on_delete=models.CASCADE, verbose_name="绘图历史")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "用户点赞"
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def delete(self, using=None, keep_parents=False):
        self.history.like_count -= 1
        self.history.save()
        super().delete()


class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    history = models.ForeignKey(DrawHistory, on_delete=models.CASCADE, verbose_name="绘图历史")
    content = models.CharField(max_length=255, verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def delete(self, using=None, keep_parents=False):
        self.history.comment_count -= 1
        self.history.save()
        super().delete()


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
