# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0089_auto_20160211_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/ioannis/rua/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='proposalformelementsrelationship',
            name='width',
            field=models.CharField(help_text=b'Horizontal Space taken by the element when rendering the form', max_length=20, choices=[(b'col-md-4', b'third'), (b'col-md-6', b'half'), (b'col-md-12', b'full')]),
        ),
    ]
