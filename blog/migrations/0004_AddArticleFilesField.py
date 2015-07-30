# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_changeImgField'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='files',
            field=models.FileField(upload_to=b'uploads/files', verbose_name='\u9644\u4ef6', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(default=b'/static/img/article/default.jpg', upload_to=b'uploads/ArticleImg', verbose_name='\u5c01\u9762\u56fe\u7247', blank=True),
        ),
        migrations.AlterField(
            model_name='carousel',
            name='img',
            field=models.ImageField(default=b'/static/img/carousel/default.jpg', upload_to=b'uploads/Carousel', verbose_name='\u8f6e\u64ad\u56fe\u7247', blank=True),
        ),
    ]
