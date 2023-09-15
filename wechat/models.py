from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class WechatUserProfile(AbstractUser):
    openid = models.CharField(max_length=255, unique=True, verbose_name='openid')
    nickname = models.CharField(max_length=255, verbose_name='昵称')
    avatar = models.URLField(verbose_name='头像')
    city = models.CharField(max_length=255, default='', verbose_name='城市')
    gender = models.CharField(max_length=255, default='', verbose_name='性别')
    province = models.CharField(max_length=255, default='', verbose_name='省份')
    token = models.CharField(max_length=255, default='', verbose_name='登录令牌')

    class Meta:
        db_table = 'wechat_user_profile'
        verbose_name = '微信用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname
