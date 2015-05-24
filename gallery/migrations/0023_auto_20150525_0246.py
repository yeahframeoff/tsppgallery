# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0022_auto_20150525_0238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibition',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание выставки', default=''),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='name',
            field=models.CharField(blank=True, default='Exhibition', max_length=32),
        ),
    ]
