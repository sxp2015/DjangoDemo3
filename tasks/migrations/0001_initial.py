# Generated by Django 4.0 on 2023-09-19 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65, unique=True, verbose_name='任务名称')),
                ('status', models.CharField(choices=[('u', '未开始'), ('o', '进行中'), ('f', '已完成')], max_length=1, verbose_name='任务状态')),
            ],
            options={
                'verbose_name': '任务管理',
                'verbose_name_plural': '任务',
            },
        ),
    ]