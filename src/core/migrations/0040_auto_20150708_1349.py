# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20150708_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='review_assignments',
            field=models.ManyToManyField(related_name='review', null=True, to='core.ReviewAssignment', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='reviewassignment',
            unique_together=set([('book', 'user', 'review_type')]),
        ),
    ]
