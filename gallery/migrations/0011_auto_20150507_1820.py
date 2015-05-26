# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0010_exhibition_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExhibitionGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('priority', models.PositiveIntegerField()),
                ('exhibition', models.ForeignKey(to='gallery.Exhibition')),
                ('genre', models.ForeignKey(to='gallery.Genre')),
            ],
        ),
        migrations.AddField(
            model_name='exhibition',
            name='genres2',
            field=models.ManyToManyField(related_name='exhibitions2', through='gallery.ExhibitionGenre', to='gallery.Genre', related_query_name='exhibition2'),
        ),
        migrations.AlterUniqueTogether(
            name='exhibitiongenre',
            unique_together=set([('exhibition', 'genre')]),
        ),
    ]
