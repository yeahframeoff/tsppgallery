# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import re


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0027_auto_20150527_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawing',
            name='name',
            field=models.CharField(verbose_name='назва', validators=[django.core.validators.RegexValidator(re.compile('^[А-Яа-яA-Za-z]+$', 32), 'Название должно содержать только буквы латинского или кириллического алфавита.', 'invalid')], max_length=32),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='description',
            field=models.TextField(verbose_name='детальний опис'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='name',
            field=models.CharField(verbose_name='назва', validators=[django.core.validators.RegexValidator(re.compile('^[А-Яа-яA-Za-z]+$', 32), 'Название должно содержать только буквы латинского или кириллического алфавита.', 'invalid')], max_length=32),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(verbose_name='first name', validators=[django.core.validators.RegexValidator('^([А-Я][а-я]+)|([A-Z][a-z]+)$', 'Имя должно быть введено в одной раскладке и начинаться с заглавной буквы', 'invalid')], max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(verbose_name='last name', validators=[django.core.validators.RegexValidator('^([А-Я][а-я]+)|([A-Z][a-z]+)$', 'Фамилия должна быть введена в одной раскладке и начинаться с заглавной буквы', 'invalid')], max_length=30, blank=True),
        ),
    ]
