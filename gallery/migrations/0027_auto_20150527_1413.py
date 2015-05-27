# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0026_auto_20150527_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawing',
            name='description',
            field=models.TextField(verbose_name='детальний опис'),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='name',
            field=models.CharField(verbose_name='назва', max_length=32),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description',
            field=models.TextField(verbose_name='Детальний опис'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='name',
            field=models.CharField(verbose_name='назва', max_length=32),
        ),
    ]
