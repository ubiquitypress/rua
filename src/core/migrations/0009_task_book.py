# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150421_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='book',
            field=models.ForeignKey(blank=True, to='core.Book', null=True),
            preserve_default=True,
        ),
    ]
