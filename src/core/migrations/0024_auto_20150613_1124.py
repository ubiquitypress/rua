# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_book_review_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='review_form',
            field=models.ForeignKey(blank=True, to='review.Form', null=True),
        ),
    ]
