# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.gauth


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20150502_1859'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', gallery.gauth.UserManager()),
            ],
        ),
    ]
