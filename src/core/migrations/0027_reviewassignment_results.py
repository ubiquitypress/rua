# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_remove_formresult_review_assignment'),
        ('core', '0026_auto_20150614_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='results',
            field=models.ForeignKey(default=1, to='review.FormResult'),
            preserve_default=False,
        ),
    ]
