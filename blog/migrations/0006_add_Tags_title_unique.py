# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_add_Tags_Table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='title',
            field=models.CharField(unique=True, max_length=30, verbose_name='\u6807\u7b7e\u540d\u79f0'),
        ),
    ]
