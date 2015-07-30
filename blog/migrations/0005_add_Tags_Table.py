# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_AddArticleFilesField'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30, verbose_name='\u6807\u7b7e\u540d\u79f0')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'ordering': ['-add_time'],
                'verbose_name': '\u6587\u7ae0\u6807\u7b7e',
                'verbose_name_plural': '\u6587\u7ae0\u6807\u7b7e',
            },
        ),
        migrations.AlterField(
            model_name='article',
            name='files',
            field=models.FileField(upload_to=b'files', verbose_name='\u9644\u4ef6', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(default=b'/static/img/article/default.jpg', upload_to=b'Article', verbose_name='\u5c01\u9762\u56fe\u7247', blank=True),
        ),
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.AlterField(
            model_name='carousel',
            name='img',
            field=models.ImageField(default=b'/static/img/carousel/default.jpg', upload_to=b'Carousel', verbose_name='\u8f6e\u64ad\u56fe\u7247', blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='blog.Tags', verbose_name='\u6807\u7b7e'),
        ),
    ]
