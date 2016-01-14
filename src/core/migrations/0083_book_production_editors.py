# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0082_contract_bpc'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='production_editors',
            field=models.ManyToManyField(related_name='production_editors', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
