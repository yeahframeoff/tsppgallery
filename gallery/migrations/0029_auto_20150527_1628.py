# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0028_auto_20150527_1534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admin',
            options={'verbose_name_plural': 'администраторы', 'verbose_name': 'администратор'},
        ),
        migrations.AlterModelOptions(
            name='drawing',
            options={'verbose_name_plural': 'картины', 'verbose_name': 'картина'},
        ),
        migrations.AlterModelOptions(
            name='exhibition',
            options={'verbose_name_plural': 'выставки', 'verbose_name': 'выставка', 'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name_plural': 'жанры', 'verbose_name': 'жанр'},
        ),
        migrations.AlterModelOptions(
            name='organizer',
            options={'verbose_name_plural': 'организаторы выставок', 'verbose_name': 'организатор выставок'},
        ),
        migrations.AlterField(
            model_name='drawing',
            name='date_uploaded',
            field=models.DateTimeField(auto_now=True, verbose_name='загружено'),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='description',
            field=models.TextField(verbose_name='детальное описание'),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='genres',
            field=models.ManyToManyField(through='gallery.DrawingGenre', verbose_name='жанры', to='gallery.Genre', related_name='drawings', related_query_name='drawing'),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='картина спрятана'),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='image',
            field=models.ImageField(verbose_name='изображение', upload_to='images/%Y/%m/'),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='name',
            field=models.CharField(verbose_name='название', max_length=32, validators=[django.core.validators.RegexValidator(re.compile('^[А-Яа-яA-Za-z\\w\\s\\.\\,]+$', 32), 'Название должно содержать только буквы латинского или кириллического алфавита.', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='drawinggenre',
            name='priority',
            field=models.PositiveIntegerField(verbose_name='приоритет'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='выставка проверена'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description',
            field=models.TextField(verbose_name='детальное описание'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='genres',
            field=models.ManyToManyField(through='gallery.ExhibitionGenre', verbose_name='жанры', to='gallery.Genre', related_name='exhibitions', related_query_name='exhibition'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='name',
            field=models.CharField(verbose_name='название', max_length=32, validators=[django.core.validators.RegexValidator(re.compile('^[А-Яа-яA-Za-z\\w\\s\\.\\,]+$', 32), 'Название должно содержать только буквы латинского или кириллического алфавита.', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='organizer',
            field=models.ForeignKey(verbose_name='организатор', to='gallery.Organizer', related_name='exhibitions', related_query_name='exhibition'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='publish_date',
            field=models.DateField(auto_now=True, verbose_name='дата публикации'),
        ),
        migrations.AlterField(
            model_name='exhibitiongenre',
            name='priority',
            field=models.PositiveIntegerField(verbose_name='приоритет'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(verbose_name='название', max_length=32),
        ),
    ]
