# Generated by Django 2.0 on 2020-02-11 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_is_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(default='', upload_to='courses/%Y/%m', verbose_name='封面'),
        ),
    ]
