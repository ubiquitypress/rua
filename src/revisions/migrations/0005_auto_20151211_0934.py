# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revisions', '0004_revision_overdue_reminder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='notes_from_editor',
            field=models.TextField(help_text=b'Enter some information to assist the author/editors with their revisions. It is best that you use full sentences in your notes.'),
        ),
    ]
