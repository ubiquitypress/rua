# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_auto_20151008_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillog',
            name='bcc',
            field=models.EmailField(default=datetime.datetime(2015, 10, 9, 11, 33, 31, 406110, tzinfo=utc), max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emaillog',
            name='cc',
            field=models.EmailField(default=datetime.datetime(2015, 10, 9, 11, 33, 38, 670648, tzinfo=utc), max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='identifier',
            name='identifier',
            field=models.CharField(max_length=20, choices=[(b'doi', b'DOI'), (b'isbn-10', b'ISBN 10'), (b'isbn-13', b'ISBN 13'), (b'urn', b'URN'), (b'pub_id', b'Publisher ID')]),
        ),
    ]
