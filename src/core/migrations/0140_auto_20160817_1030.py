# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0139_auto_20160815_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emaillog',
            name='attachment',
        ),
        migrations.AddField(
            model_name='emaillog',
            name='attachments',
            field=models.ManyToManyField(related_name='email_attachments', null=True, to='core.File', blank=True),
        ),
        migrations.AlterField(
            model_name='identifier',
            name='identifier',
            field=models.CharField(max_length=20, choices=[(b'doi', b'DOI'), (b'isbn-10', b'ISBN 10'), (b'isbn-13', b'ISBN 13'), (b'issn', b'ISSN'), (b'urn', b'URN'), (b'pub_id', b'Publisher ID')]),
        ),
    ]
