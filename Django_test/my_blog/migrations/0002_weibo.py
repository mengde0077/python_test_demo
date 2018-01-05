# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weibo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('massage', models.CharField(max_length=200)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='my_blog.Author')),
            ],
        ),
    ]
