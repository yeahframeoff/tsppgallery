# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def main_op(apps, schema_editor):
    """
    Populates models.Drawing.genres2 to Genre intermediate
    table for many-to-many relationship from existing
    models.Drawing.genres relationship
    """
    Drawing = apps.get_model('gallery', 'Drawing')
    DrawingGenreNew = apps.get_model('gallery', 'DrawingGenre')
    DrawingGenreNew.objects.all().delete()
    drawings = Drawing.objects.all()
    for drawing in drawings:
        bulk = []
        drawing_genres = \
            drawing.genres.all()
        i = 0
        for genre in drawing_genres:
            i += 1
            bulk.append(DrawingGenreNew(drawing=drawing, genre=genre, priority=i))
        DrawingGenreNew.objects.bulk_create(bulk)


def reverse_op(apps, schema_editor):
    """
    Populates back models.Drawing.genres from
    models.Drawing.genres2 relationship
    """
    Drawing = apps.get_model('gallery', 'Drawing')
    DrawingGenreOld = Drawing.genres.through
    DrawingGenreNew = apps.get_model('gallery', 'DrawingGenre')
    DrawingGenreOld.objects.all().delete()
    pivots = \
        [
            DrawingGenreOld(
                genre=x.genre,
                drawing=x.drawing
            )
            for x in DrawingGenreNew.objects.all()
        ]
    DrawingGenreOld.objects.bulk_create(pivots)


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0015_auto_20150508_1815'),
        ]

    operations = [
        migrations.RunPython(main_op, reverse_op)
    ]
