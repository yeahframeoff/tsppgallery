# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0019_auto_20150508_1821'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name_plural': 'genres', 'verbose_name': 'genre'},
        ),
    ]
