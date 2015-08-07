# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_auto_20150802_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1000)),
                ('notes', models.TextField(null=True, blank=True)),
                ('editor_signed_off', models.DateField(null=True, blank=True)),
                ('author_signed_off', models.DateField(null=True, blank=True)),
                ('file', models.ForeignKey(to='core.File')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='misc_files',
            field=models.ManyToManyField(related_name='misc_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='contract',
            field=models.ForeignKey(blank=True, to='core.Contract', null=True),
        ),
    ]
