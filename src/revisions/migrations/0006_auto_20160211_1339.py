# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revisions', '0005_auto_20151211_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='notes_from_editor',
            field=models.TextField(help_text=b'These notes should be as clear as possible to instruct the author on the revisions required. The notes will be displayed to the author.'),
        ),
    ]
