# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0009_drawing_date_uploaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibition',
            name='description',
            field=models.TextField(verbose_name='описание выставки', default=''),
            preserve_default=False,
        ),
    ]
