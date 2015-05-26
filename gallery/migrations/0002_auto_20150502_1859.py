# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.gauth


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', gallery.gauth.Role(blank=True, help_text='The role this user belongs to. A user will get all permissions granted to this role', choices=[('AD', 'Admin'), ('AR', 'Artist'), ('OR', 'Organizer')], verbose_name='groups', default='AR', max_length=2)),
                ('permission', models.ForeignKey(to='auth.Permission', verbose_name='role_perm')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=gallery.gauth.Role(blank=True, help_text='The role this user belongs to. A user will get all permissions granted to this role', choices=[('AD', 'Admin'), ('AR', 'Artist'), ('OR', 'Organizer')], verbose_name='groups', default='AR', max_length=2),
        ),
    ]
