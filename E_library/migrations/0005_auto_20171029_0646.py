# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 01:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('E_library', '0004_auto_20171029_0600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='bookgenre',
        ),
        migrations.AddField(
            model_name='genre_allot',
            name='Isbn',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='E_library.Book'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='genre_allot',
            unique_together=set([('Isbn', 'genre')]),
        ),
    ]
