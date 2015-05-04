# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20150502_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
            ],
            options={
                'abstract': False,
                'proxy': True,
            },
            bases=('gallery.user',),
            managers=[
                ('objects', gallery.models.AdminManager()),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
            ],
            options={
                'abstract': False,
                'proxy': True,
            },
            bases=('gallery.user',),
            managers=[
                ('objects', gallery.models.ArtistManager()),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
            ],
            options={
                'abstract': False,
                'proxy': True,
            },
            bases=('gallery.user',),
            managers=[
                ('objects', gallery.models.OrganizerManager()),
            ],
        ),
    ]
