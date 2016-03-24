# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('submission', '0018_historyproposal_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyproposal',
            name='user_edited',
            field=models.ForeignKey(related_name='edited_by_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
