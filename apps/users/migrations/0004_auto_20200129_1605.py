# Generated by Django 3.0.2 on 2020-01-29 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200129_1602'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='birday',
            new_name='birthday',
        ),
    ]
