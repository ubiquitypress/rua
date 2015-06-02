# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150531_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('types', models.CharField(max_length=20, choices=[(b'rich_text', b'Rich Text'), (b'text', b'Text'), (b'char', b'Characters'), (b'number', b'Number'), (b'boolean', b'Boolean'), (b'file', b'File')])),
                ('value', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SettingGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='fileversion',
            options={'ordering': ('-date_uploaded',)},
        ),
        migrations.AddField(
            model_name='setting',
            name='group',
            field=models.ForeignKey(to='core.SettingGroup'),
        ),
    ]
