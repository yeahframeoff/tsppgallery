# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0008_auto_20150506_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawing',
            name='date_uploaded',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 5, 23, 14, 26, 825235, tzinfo=utc), auto_now=True, verbose_name='загружено'),
            preserve_default=False,
        ),
    ]
