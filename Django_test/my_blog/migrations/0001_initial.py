# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('descript', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('recommend', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to='my_blog.Author')),
            ],
            options={
                'ordering': ['-publish_time'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag_name', models.CharField(max_length=20)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(to='my_blog.Tag', blank=True),
        ),
    ]
