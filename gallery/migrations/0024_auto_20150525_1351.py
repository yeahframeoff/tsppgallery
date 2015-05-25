# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0023_auto_20150525_0246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admin',
            options={'verbose_name': 'адміністратор', 'verbose_name_plural': 'адміністратори'},
        ),
        migrations.AlterModelOptions(
            name='artist',
            options={'verbose_name': 'художник', 'verbose_name_plural': 'художники'},
        ),
        migrations.AlterModelOptions(
            name='drawing',
            options={'verbose_name': 'малюнок', 'verbose_name_plural': 'малюнки'},
        ),
        migrations.AlterModelOptions(
            name='exhibition',
            options={'verbose_name': 'виставка', 'verbose_name_plural': 'виставки', 'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'жанр', 'verbose_name_plural': 'жанри'},
        ),
        migrations.AlterModelOptions(
            name='organizer',
            options={'verbose_name': 'організатор виставок', 'verbose_name_plural': 'організатори виставок'},
        ),
        migrations.AlterField(
            model_name='drawing',
            name='artist',
            field=models.ForeignKey(verbose_name='художник', to='gallery.Artist', related_name='drawings', related_query_name='drawing'),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='date_uploaded',
            field=models.DateTimeField(verbose_name='завантажено', auto_now=True),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='description',
            field=models.TextField(verbose_name='детальний опис', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='genres',
            field=models.ManyToManyField(verbose_name='жанри', related_query_name='drawing', through='gallery.DrawingGenre', to='gallery.Genre', related_name='drawings'),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='hidden',
            field=models.BooleanField(verbose_name='малюнок сховано', default=False),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='image',
            field=models.ImageField(verbose_name='зображення', upload_to='images/%Y/%m/'),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='name',
            field=models.CharField(verbose_name='назва', default='Drawing', blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='drawinggenre',
            name='genre',
            field=models.ForeignKey(verbose_name='жанр', to='gallery.Genre'),
        ),
        migrations.AlterField(
            model_name='drawinggenre',
            name='priority',
            field=models.PositiveIntegerField(verbose_name='приорітет'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='approved',
            field=models.BooleanField(verbose_name='перевірено', default=False),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description',
            field=models.TextField(verbose_name='Детальний опис', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='genres',
            field=models.ManyToManyField(verbose_name='жанри', related_query_name='exhibition', through='gallery.ExhibitionGenre', to='gallery.Genre', related_name='exhibitions'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='name',
            field=models.CharField(verbose_name='назва', default='Exhibition', blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='organizer',
            field=models.ForeignKey(verbose_name='організатор', to='gallery.Organizer', related_name='exhibitions', related_query_name='exhibition'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='publish_date',
            field=models.DateField(verbose_name='дата публікації', auto_now=True),
        ),
        migrations.AlterField(
            model_name='exhibitiongenre',
            name='genre',
            field=models.ForeignKey(verbose_name='жанр', to='gallery.Genre'),
        ),
        migrations.AlterField(
            model_name='exhibitiongenre',
            name='priority',
            field=models.PositiveIntegerField(verbose_name='приорітет'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(verbose_name='назва', max_length=32),
        ),
    ]
