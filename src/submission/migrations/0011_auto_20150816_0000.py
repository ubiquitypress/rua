# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20150816_0000'),
        ('submission', '0010_auto_20150802_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='description',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='funding',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='subtitle',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='title',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='uploaded_file',
        ),
        migrations.AddField(
            model_name='proposal',
            name='data',
            field=models.TextField(default='data'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposal',
            name='form',
            field=models.ForeignKey(default=1, to='core.ProposalForm'),
            preserve_default=False,
        ),
    ]
