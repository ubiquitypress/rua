# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('submission', '0017_historyproposal'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyproposal',
            name='owner',
            field=models.ForeignKey(related_name='parent_proposal_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
