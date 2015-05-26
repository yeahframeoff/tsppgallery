# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0024_auto_20150525_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibition',
            name='approved',
            field=models.BooleanField(verbose_name='виставку перевірено', default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(verbose_name='first name', blank=True, validators=[django.core.validators.RegexValidator('^[А-Яа-яA-Z][a-z]+$', 'Enter a valid name. This value may contain only small and capital letters.', 'invalid')], max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(verbose_name='last name', blank=True, validators=[django.core.validators.RegexValidator('^[А-Яа-яA-Z][a-z]+$', 'Enter a valid name. This value may contain only small and capital letters.', 'invalid')], max_length=30),
        ),
    ]
