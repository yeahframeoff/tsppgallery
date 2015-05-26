# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0014_auto_20150507_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrawingGenre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('priority', models.PositiveIntegerField()),
                ('drawing', models.ForeignKey(to='gallery.Drawing')),
            ],
            options={
                'ordering': ('drawing_id', 'priority'),
            },
        ),
        migrations.AlterModelOptions(
            name='exhibition',
            options={'verbose_name': 'exhibition', 'ordering': ('id',), 'verbose_name_plural': 'exhibitions'},
        ),
        migrations.AlterModelOptions(
            name='exhibitiongenre',
            options={'ordering': ('exhibition_id', 'priority')},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'genre', 'ordering': ('exhibitiongenre__priority',), 'verbose_name_plural': 'genres'},
        ),
        migrations.AddField(
            model_name='drawinggenre',
            name='genre',
            field=models.ForeignKey(to='gallery.Genre'),
        ),
        migrations.AddField(
            model_name='drawing',
            name='genres2',
            field=models.ManyToManyField(through='gallery.DrawingGenre', to='gallery.Genre', related_query_name='drawing2', related_name='drawings2'),
        ),
        migrations.AlterUniqueTogether(
            name='drawinggenre',
            unique_together=set([('drawing', 'genre')]),
        ),
    ]
