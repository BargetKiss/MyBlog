# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('litdev_auth', '0004_AddArticleFilesField'),
    ]

    operations = [
        migrations.AlterField(
            model_name='litdevuser',
            name='img',
            field=models.ImageField(default=b'/static/tx/default.jpg', upload_to=b'HeadImg', verbose_name='\u5934\u50cf\u5730\u5740', blank=True),
        ),
    ]
