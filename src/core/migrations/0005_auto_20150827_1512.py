# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150827_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalformelementsrelationship',
            name='width',
            field=models.CharField(default='col-md-12', help_text=b'Vertical Space taken by the element when rendering the form', max_length=20, choices=[(b'col-md-4', b'third'), (b'col-md-6', b'half'), (b'col-md-12', b'full')]),
            preserve_default=False,
        ),
    ]
