# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0012_auto_20150507_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exhibition',
            name='genres',
        ),
    ]
