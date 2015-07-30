# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='News',
        ),
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.CharField(default=b'/static/img/article/default.jpg', max_length=200, verbose_name='\u5c01\u9762\u56fe\u7247'),
        ),
    ]
