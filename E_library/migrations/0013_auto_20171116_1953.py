# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 14:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('E_library', '0012_auto_20171116_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='user_type',
            field=models.OneToOneField(blank=True, max_length=4, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_type',
            field=models.OneToOneField(blank=True, max_length=4, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]