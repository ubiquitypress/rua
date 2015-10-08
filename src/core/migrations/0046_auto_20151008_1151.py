# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_auto_20151007_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/Users/ioanniscleary/Code/rua/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='typesetassignment',
            name='typesetter_files',
            field=models.ManyToManyField(related_name='typesetter_files', null=True, to='core.File', blank=True),
        ),
    ]
