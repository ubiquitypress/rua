# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0102_auto_20160317_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='editorial_review_assignments',
            field=models.ManyToManyField(related_name='editorial_review', null=True, to='core.EditorialReviewAssignment', blank=True),
        ),
    ]
