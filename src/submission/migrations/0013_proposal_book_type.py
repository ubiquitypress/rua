# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0012_auto_20160315_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='book_type',
            field=models.CharField(blank=True, max_length=50, null=True, help_text=b'A monograph is a work authored, in its entirety, by one or more authors. An edited volume has different authors for each chapter.', choices=[(b'monograph', b'Monograph'), (b'edited_volume', b'Edited Volume')]),
        ),
    ]
