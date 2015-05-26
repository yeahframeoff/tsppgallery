# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0017_remove_drawing_genres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drawing',
            name='genres2',
        ),
        migrations.AddField(
            model_name='drawing',
            name='genres',
            field=models.ManyToManyField(related_name='drawings', to='gallery.Genre', related_query_name='drawing', through='gallery.DrawingGenre'),
        ),
    ]
