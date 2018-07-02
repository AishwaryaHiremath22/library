# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 15:20
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_library', '0014_auto_20171116_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='Price',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='borrows',
            name='ratings',
            field=models.FloatField(validators=[django.core.validators.RegexValidator('^[0-10]$', 'Enter ratings 0-10.')]),
        ),
    ]
