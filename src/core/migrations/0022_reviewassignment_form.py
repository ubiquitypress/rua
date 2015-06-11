# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
        ('core', '0021_reviewassignment_due'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='form',
            field=models.ForeignKey(default='1', to='review.Form'),
            preserve_default=False,
        ),
    ]
