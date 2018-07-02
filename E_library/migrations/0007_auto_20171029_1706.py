# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 11:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('E_library', '0006_auto_20171029_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='A_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='E_library.Author'),
        ),
        migrations.AlterUniqueTogether(
            name='genre_allot',
            unique_together=set([('Isbn', 'genre')]),
        ),
    ]
