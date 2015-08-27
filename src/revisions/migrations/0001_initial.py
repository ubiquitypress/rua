# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150816_0101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cover_letter', models.TextField(null=True, blank=True)),
                ('revision_type', models.CharField(max_length=100, choices=[(b'submission', b'Submission'), (b'review', b'Review')])),
                ('requested', models.DateField(auto_now_add=True)),
                ('due', models.DateField(null=True, blank=True)),
                ('completed', models.DateField(null=True, blank=True)),
                ('book', models.ForeignKey(to='core.Book')),
            ],
        ),
    ]
