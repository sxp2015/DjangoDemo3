from django.db import models


# Create your models here.
class Status(models.TextChoices):
    UN_STARTED = 'u', "未开始"
    ONGOING = 'o', "进行中"
    FINISHED = 'f', "已完成"


class Task(models.Model):
    name = models.CharField(verbose_name="任务名称", max_length=65, unique=True)
    status = models.CharField(verbose_name="任务状态", max_length=1, choices=Status.choices)

    class Meta:
        verbose_name = "任务管理"
        verbose_name_plural = "任务"

    def __str__(self):
        return self.name
