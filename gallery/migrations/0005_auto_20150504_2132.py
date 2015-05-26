# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_admin_artist_organizer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drawing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('image', models.ImageField(upload_to='images/%Y/%m/')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('hidden', models.BooleanField(verbose_name='спрятано', default=False)),
                ('artist', models.ForeignKey(to='gallery.Artist', related_name='drawings', related_query_name='drawing')),
            ],
        ),
        migrations.CreateModel(
            name='Exhibition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('publish_date', models.DateField(auto_now=True)),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(verbose_name='user photo', null=True, upload_to='userphotos'),
        ),
        migrations.AddField(
            model_name='exhibition',
            name='genres',
            field=models.ManyToManyField(to='gallery.Genre', related_name='exhibitions', related_query_name='exhibition'),
        ),
        migrations.AddField(
            model_name='exhibition',
            name='images',
            field=models.ManyToManyField(to='gallery.Drawing', related_name='exhibitions', related_query_name='exhibition'),
        ),
        migrations.AddField(
            model_name='exhibition',
            name='organizer',
            field=models.ForeignKey(to='gallery.Organizer', related_name='exhibitions', related_query_name='exhibition'),
        ),
        migrations.AddField(
            model_name='drawing',
            name='genres',
            field=models.ManyToManyField(to='gallery.Genre', related_name='drawings', related_query_name='drawing'),
        ),
    ]
