# Generated by Django 2.0 on 2020-02-06 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20200204_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='python', max_length=100, verbose_name='课程类别'),
        ),
    ]
