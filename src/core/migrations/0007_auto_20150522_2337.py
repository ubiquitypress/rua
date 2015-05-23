# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150522_2044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ('sequence', 'kind')},
        ),
        migrations.AlterField(
            model_name='series',
            name='editor',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
