# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0109_auto_20160321_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIConnector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=255, null=True, blank=True)),
                ('username', models.CharField(max_length=256, null=True, blank=True)),
                ('password', models.CharField(max_length=512, null=True, blank=True)),
            ],
        ),
    ]
