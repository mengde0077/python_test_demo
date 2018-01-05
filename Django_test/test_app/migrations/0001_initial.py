# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='\u6807\u9898')),
                ('slug', models.CharField(max_length=256, verbose_name='\u7f51\u5740', db_index=True)),
                ('content', models.TextField(default='', verbose_name='\u5185\u5bb9', blank=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u8868\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', null=True)),
                ('author', models.ForeignKey(verbose_name='\u4f5c\u8005', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u6559\u7a0b',
                'verbose_name_plural': '\u6559\u7a0b',
            },
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='\u680f\u76ee\u540d\u79f0')),
                ('slug', models.CharField(max_length=256, verbose_name='\u680f\u76ee\u7f51\u5740', db_index=True)),
                ('intro', models.TextField(default='', verbose_name='\u680f\u76ee\u7b80\u4ecb')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u680f\u76ee',
                'verbose_name_plural': '\u680f\u76ee',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='column',
            field=models.ManyToManyField(to='test_app.Column', verbose_name='\u5f52\u5c5e\u680f\u76ee'),
        ),
    ]
