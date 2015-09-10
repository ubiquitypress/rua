# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20150907_0900'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('to', models.EmailField(max_length=1000)),
                ('from_address', models.EmailField(max_length=1000)),
                ('subject', models.CharField(max_length=1000)),
                ('content', models.TextField()),
                ('book', models.ForeignKey(to='core.Book')),
            ],
        ),
    ]
