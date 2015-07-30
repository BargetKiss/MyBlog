# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_add_Tags_title_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name='\u8bc4\u8bba\u8005\u90ae\u7bb1')),
                ('nick_name', models.CharField(max_length=20, verbose_name='\u6635\u79f0')),
                ('ip', models.CharField(max_length=100, verbose_name='\u8bc4\u8bba\u7684IP')),
                ('comment', models.TextField(verbose_name='\u5185\u5bb9')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u8bc4\u8bba\u65f6\u95f4')),
                ('article', models.ForeignKey(verbose_name='\u6587\u7ae0', to='blog.Article')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u8bc4\u8bba',
                'verbose_name_plural': '\u8bc4\u8bba',
            },
        ),
    ]
