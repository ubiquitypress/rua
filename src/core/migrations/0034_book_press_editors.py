# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0033_auto_20150915_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='press_editors',
            field=models.ManyToManyField(related_name='press_editors', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
