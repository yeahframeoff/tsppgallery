# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_auto_20150505_2351'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drawing',
            options={'verbose_name_plural': 'drawings', 'verbose_name': 'drawing'},
        ),
        migrations.AlterModelOptions(
            name='exhibition',
            options={'verbose_name_plural': 'exhibitions', 'verbose_name': 'exhibition'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name_plural': 'genres', 'verbose_name': 'genre'},
        ),
        migrations.AlterModelOptions(
            name='organizer',
            options={'verbose_name_plural': 'organizers', 'verbose_name': 'organizer'},
        ),
    ]
