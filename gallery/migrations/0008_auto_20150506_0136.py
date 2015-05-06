# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_auto_20150506_0117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exhibition',
            old_name='images',
            new_name='drawings',
        ),
    ]
