# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0011_auto_20160308_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalreview',
            name='comments_from_editor',
            field=models.TextField(help_text=b'If any editors have any comments for the reviewer', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='proposalreview',
            name='reopened',
            field=models.BooleanField(default=False),
        ),
    ]
