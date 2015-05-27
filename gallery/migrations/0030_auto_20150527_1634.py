# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import re


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0029_auto_20150527_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(verbose_name='название', max_length=32, validators=[django.core.validators.RegexValidator(re.compile('^[А-Яа-яA-Za-z\\w\\s\\.\\,]+$', 32), 'Название должно содержать только буквы латинского или кириллического алфавита.', 'invalid')]),
        ),
    ]
