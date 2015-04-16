# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150416_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/mauro/Projects/smw/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
            preserve_default=True,
        ),
    ]
