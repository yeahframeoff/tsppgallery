# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0013_remove_exhibition_genres'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exhibition',
            old_name='genres2',
            new_name='genres',
        ),
    ]
