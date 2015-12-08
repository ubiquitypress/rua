# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0064_auto_20151105_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_editors',
            field=models.ManyToManyField(related_name='book_editors', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
