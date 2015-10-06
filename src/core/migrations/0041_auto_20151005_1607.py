# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models
from django.utils.timezone import utc
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewround',
            name='date_started',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 5, 16, 7, 20, 20040, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/Users/andy/Code/rua/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
        ),
    ]
