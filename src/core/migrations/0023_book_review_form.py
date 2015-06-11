# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_auto_20150611_2039'),
        ('core', '0022_reviewassignment_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='review_form',
            field=models.ForeignKey(default=1, to='review.Form'),
            preserve_default=False,
        ),
    ]
