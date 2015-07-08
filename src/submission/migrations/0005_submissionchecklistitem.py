# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0004_proposal_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmissionChecklistItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=500)),
                ('sequence', models.IntegerField(default=999)),
                ('required', models.BooleanField(default=True)),
            ],
        ),
    ]
