# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0018_auto_20150508_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibition',
            name='genres',
            field=models.ManyToManyField(related_name='exhibitions', related_query_name='exhibition', through='gallery.ExhibitionGenre', to='gallery.Genre'),
        ),
    ]
