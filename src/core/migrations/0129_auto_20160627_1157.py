# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0128_auto_20160517_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='authors',
            field=models.ManyToManyField(to='core.Author', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='table_contents',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'book-level', b'Book Level'), (b'chapter-level', b'Chapter Level')]),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='blurbs',
            field=models.TextField(null=True, verbose_name=b'blurb', blank=True),
        ),
    ]
