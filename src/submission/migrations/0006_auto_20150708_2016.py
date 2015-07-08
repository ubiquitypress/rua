# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0005_submissionchecklistitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submissionchecklistitem',
            options={'ordering': ('sequence', 'text')},
        ),
        migrations.AddField(
            model_name='submissionchecklistitem',
            name='slug',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
    ]
