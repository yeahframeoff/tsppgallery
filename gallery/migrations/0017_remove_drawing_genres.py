# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0016_auto_20150508_1816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drawing',
            name='genres',
        ),
    ]
