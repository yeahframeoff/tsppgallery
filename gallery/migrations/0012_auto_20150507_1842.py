# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def main_op(apps, schema_editor):
    """
    Populates models.Exhibition.genres2 to Genre intermediate
    table for many-to-many relationship from existing
    models.Exhibition.genres relationship
    """
    Exhibition = apps.get_model('gallery', 'Exhibition')
    ExhibitionGenreNew = apps.get_model('gallery', 'ExhibitionGenre')
    ExhibitionGenreNew.objects.all().delete()
    exhibitions = Exhibition.objects.all()
    for xzibit in exhibitions:
        bulk = []
        xzibit_genres = \
            xzibit.genres.all()
        i = 0
        for genre in xzibit_genres:
            i += 1
            bulk.append(ExhibitionGenreNew(exhibition=xzibit, genre=genre, priority=i))
        ExhibitionGenreNew.objects.bulk_create(bulk)



def reverse_op(apps, schema_editor):
    """
    Populates back models.Exhibition.genres from
    models.Exhibition.genres2 relationship
    """
    Exhibition = apps.get_model('gallery', 'Exhibition')
    ExhibitionGenreOld = Exhibition.genres.through
    ExhibitionGenreNew = apps.get_model('gallery', 'ExhibitionGenre')
    ExhibitionGenreOld.objects.all().delete()
    pivots = \
        [
            ExhibitionGenreOld(
                genre=x.genre,
                exhibition=x.exhibition
            )
            for x in ExhibitionGenreNew.objects.all()
        ]
    ExhibitionGenreOld.objects.bulk_create(pivots)


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0011_auto_20150507_1820'),
        ]

    operations = [
        migrations.RunPython(main_op, reverse_op)
    ]
