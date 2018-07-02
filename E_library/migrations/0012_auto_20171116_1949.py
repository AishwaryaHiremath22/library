# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 14:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('E_library', '0011_auto_20171115_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='user_type',
            field=models.OneToOneField(default=None, max_length=4, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='user_type',
            field=models.OneToOneField(default=None, max_length=4, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
