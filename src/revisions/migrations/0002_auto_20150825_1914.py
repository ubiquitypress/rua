# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revisions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='revision',
            name='notes_from_editor',
            field=models.TextField(default='', help_text=b'Enter some information to assist the author/editors with their revisions.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='revision',
            name='due',
            field=models.DateField(help_text=b'Set the date the revisions are due. The author will be reminded once before the due date and once after.', null=True, blank=True),
        ),
    ]
