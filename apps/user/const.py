from django.db.models import IntegerChoices
from enum import unique


@unique
class RewardTypeChoices(IntegerChoices):
    # 收支分类
    SIGN_IN = 0, "签到"
    SHARE = 1, "分享"
    RECHARGE = 2, "充值"
    DRAW = 3, "绘图"
