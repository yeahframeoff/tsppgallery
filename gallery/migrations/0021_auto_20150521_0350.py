# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0020_auto_20150508_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawing',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='name',
            field=models.CharField(default='Drawing', max_length=32, blank=True),
        ),
    ]
