from django.db import models


# Create your models here.
class UserInfo(models.Model):
    phone = models.CharField(max_length=11, verbose_name='手机号', unique=True)
    token = models.CharField(max_length=300, verbose_name='用户Token', null=True, blank=True)
