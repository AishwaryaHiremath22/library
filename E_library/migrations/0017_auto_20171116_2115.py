# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_library', '0016_auto_20171116_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='user_type',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_type',
            field=models.IntegerField(default=1),
        ),
    ]
