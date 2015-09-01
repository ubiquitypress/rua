# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_copyeditassignment_indexassignment_typesetassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='copyeditassignment',
            name='requested',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 16, 18, 9, 82141, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='indexassignment',
            name='requested',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 16, 18, 14, 434563, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='requested',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 16, 18, 18, 50658, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='log',
            name='kind',
            field=models.CharField(max_length=100, choices=[(b'submission', b'Submission'), (b'workflow', b'Workflow'), (b'file', b'File'), (b'copyedit', b'Copyedit'), (b'review', b'Review'), (b'index', b'Index'), (b'typeset', b'Typeset')]),
        ),
    ]
