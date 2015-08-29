# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=20, choices=[(b'doi', b'DOI'), (b'isbn-10', b'ISBN 10'), (b'isbn-13', b'ISBN 13'), (b'urn', b'URN')])),
                ('value', models.CharField(max_length=300)),
                ('displayed', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrintSales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='doi',
        ),
        migrations.AddField(
            model_name='printsales',
            name='book',
            field=models.ForeignKey(to='core.Book'),
        ),
        migrations.AddField(
            model_name='identifier',
            name='book',
            field=models.ForeignKey(to='core.Book'),
        ),
    ]
