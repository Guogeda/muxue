# Generated by Django 3.0.2 on 2020-01-29 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_banner_emailverfyrecode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', '男性'), ('female', '女性')], default='female', max_length=7),
        ),
    ]
