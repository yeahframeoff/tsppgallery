# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0021_auto_20150521_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^[A-Z][a-z]+$', 'Enter a valid name. This value may contain only small and capital letters.', 'invalid')], verbose_name='first name', blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^[A-Z][a-z]+$', 'Enter a valid name. This value may contain only small and capital letters.', 'invalid')], verbose_name='last name', blank=True, max_length=30),
        ),
    ]
