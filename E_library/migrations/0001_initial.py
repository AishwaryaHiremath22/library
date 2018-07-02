# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 00:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fname', models.CharField(max_length=50)),
                ('Mname', models.CharField(blank=True, max_length=50)),
                ('Lname', models.CharField(max_length=50)),
                ('Password', models.CharField(max_length=15)),
                ('Email_id', models.EmailField(max_length=254, unique=True)),
                ('Phone_no', models.CharField(max_length=10)),
                ('Picture', models.FileField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='belongs_to',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('Isbn', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=50)),
                ('Copy', models.FileField(upload_to='')),
                ('Cover', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='borrows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.FloatField()),
                ('Isbn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_library.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateE', models.DateField()),
                ('E_title', models.CharField(max_length=50)),
                ('Picture', models.FileField(blank=True, upload_to='')),
                ('Location', models.CharField(max_length=500)),
                ('A_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_library.Author')),
            ],
        ),
        migrations.CreateModel(
            name='event_genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Genre', models.CharField(max_length=50)),
                ('Title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_library.Event')),
            ],
        ),
        migrations.CreateModel(
            name='genre_allot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('Group_id', models.IntegerField(primary_key=True, serialize=False)),
                ('Genre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fname', models.CharField(max_length=50)),
                ('Mname', models.CharField(blank=True, max_length=50)),
                ('Lname', models.CharField(max_length=50)),
                ('Password', models.CharField(max_length=15)),
                ('Email_id', models.EmailField(max_length=254, unique=True)),
                ('Phone_no', models.CharField(max_length=10)),
                ('Picture', models.FileField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='written_by',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('A_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_library.Author')),
                ('Isbn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_library.Book')),
            ],
        ),
        migrations.AddField(
            model_name='borrows',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_library.Users'),
        ),
        migrations.AddField(
            model_name='book',
            name='bookgenre',
            field=models.ManyToManyField(blank=True, null=True, to='E_library.genre_allot'),
        ),
        migrations.AddField(
            model_name='belongs_to',
            name='G_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_library.Group'),
        ),
        migrations.AddField(
            model_name='belongs_to',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_library.Users'),
        ),
        migrations.AlterUniqueTogether(
            name='written_by',
            unique_together=set([('A_id', 'Isbn')]),
        ),
        migrations.AlterUniqueTogether(
            name='event_genre',
            unique_together=set([('Title', 'Genre')]),
        ),
        migrations.AlterUniqueTogether(
            name='borrows',
            unique_together=set([('user_id', 'Isbn')]),
        ),
        migrations.AlterUniqueTogether(
            name='belongs_to',
            unique_together=set([('G_id', 'user_id')]),
        ),
    ]
