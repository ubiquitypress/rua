# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('submission', '0023_auto_20160401_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='book_editors',
            field=models.ManyToManyField(related_name='proposal_book_editors', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
