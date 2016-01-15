# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0084_book_expected_completion_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='read_only_users',
            field=models.ManyToManyField(related_name='read_only_users', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='competing_interests',
            field=models.TextField(help_text=b"If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'. <a href='/page/competing_interests/'>More info</a>", null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reviewassignment',
            name='competing_interests',
            field=models.TextField(help_text=b"If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'. <a href='/page/competing_interests/'>More info</a>", null=True, blank=True),
        ),
    ]
