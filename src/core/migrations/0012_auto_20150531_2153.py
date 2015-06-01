# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_license_version'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_filename', models.CharField(max_length=1000)),
                ('uuid_filename', models.CharField(max_length=100)),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('date_uploaded',),
            },
        ),
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ('sequence', '-kind')},
        ),
        migrations.AddField(
            model_name='fileversion',
            name='file',
            field=models.ForeignKey(to='core.File'),
        ),
    ]
