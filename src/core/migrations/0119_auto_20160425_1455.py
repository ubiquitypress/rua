# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0118_remove_contract_proposal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(help_text=b'This is used for metadata, the website text and the back cover of the book', max_length=5000, null=True, verbose_name=b'Book Summary', blank=True),
        ),
    ]
