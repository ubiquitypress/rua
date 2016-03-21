# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0108_auto_20160318_1139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editorialreviewassignment',
            name='files',
        ),
        migrations.AddField(
            model_name='editorialreviewassignment',
            name='editorial_board_files',
            field=models.ManyToManyField(related_name='editorial_board_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='editorialreviewassignment',
            name='publication_committee_files',
            field=models.ManyToManyField(related_name='publication_committee_files', null=True, to='core.File', blank=True),
        ),
    ]
