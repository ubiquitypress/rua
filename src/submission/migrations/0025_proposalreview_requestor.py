# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('submission', '0024_proposal_book_editors'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalreview',
            name='requestor',
            field=models.ForeignKey(related_name='review_requestor', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
