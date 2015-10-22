# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20150902_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='fields',
        ),
        migrations.AddField(
            model_name='form',
            name='form_fields',
            field=models.ManyToManyField(related_name='form_fields', to='review.FormElementsRelationship', blank=True),
        ),
    ]
