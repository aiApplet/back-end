from django.db.models import IntegerChoices
from enum import unique


@unique
class DrawHistoryStatusChoices(IntegerChoices):
    # 收支分类
    IN_WORK = 0, "进行中"
    SUCCESS = 1, "成功"
    FAIL = 2, "失败"
