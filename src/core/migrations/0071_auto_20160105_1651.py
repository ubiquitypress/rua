# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0070_copyeditassignment_note_from_copyeditor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='book',
            field=models.ForeignKey(blank=True, to='core.Book', null=True),
        ),
    ]
