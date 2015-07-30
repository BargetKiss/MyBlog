# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('litdev_auth', '0002_check_user_img_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='litdevuser',
            options={'verbose_name': '\u7528\u6237\u62d3\u5c55\u4fe1\u606f', 'verbose_name_plural': '\u7528\u6237\u62d3\u5c55\u4fe1\u606f'},
        ),
        migrations.AlterField(
            model_name='litdevuser',
            name='img',
            field=models.ImageField(default=b'/static/tx/default.jpg', upload_to=b'/uploads/HeadImg', verbose_name='\u5934\u50cf\u5730\u5740', blank=True),
        ),
    ]
