# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0141_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emaillog',
            name='attachments',
        ),
        migrations.AddField(
            model_name='emaillog',
            name='attachment',
            field=models.ManyToManyField(related_name='email_attachment', null=True, to='core.File', blank=True),
        ),
    ]
