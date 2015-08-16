# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_auto_20150809_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='author_file',
            field=models.ForeignKey(related_name='author_file', blank=True, to='core.File', null=True),
        ),
    ]
