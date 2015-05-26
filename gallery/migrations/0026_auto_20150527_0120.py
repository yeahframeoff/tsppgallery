# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0025_auto_20150526_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Required. 4-20 characters. Small letters, digits,dot and underscore characters.', validators=[django.core.validators.RegexValidator('^[A-Za-z0-9._]{4,20}$', 'Enter a valid username. This value may contain only small letters, digits, dot and underscore characters. From 4 up to 20 characters.', 'invalid')], max_length=20, unique=True, error_messages={'unique': 'A user with that username already exists.'}, verbose_name='username'),
        ),
    ]
