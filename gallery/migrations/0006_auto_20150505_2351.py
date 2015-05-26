# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_auto_20150504_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Biography'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(upload_to='userphotos', null=True, verbose_name='User photo'),
        ),
    ]
