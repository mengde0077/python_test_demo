# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_blog', '0002_weibo'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='read_num',
            field=models.IntegerField(default=0),
        ),
    ]
