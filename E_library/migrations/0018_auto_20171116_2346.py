# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 18:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('E_library', '0017_auto_20171116_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='user_type',
        ),
        migrations.RemoveField(
            model_name='users',
            name='user_type',
        ),
    ]