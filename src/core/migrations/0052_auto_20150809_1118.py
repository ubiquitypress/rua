# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_auto_20150804_2254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='file',
        ),
        migrations.AddField(
            model_name='contract',
            name='author_file',
            field=models.ForeignKey(related_name='author_file', default=1, to='core.File'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='editor_file',
            field=models.ForeignKey(related_name='editor_file', blank=True, to='core.File', null=True),
        ),
    ]
