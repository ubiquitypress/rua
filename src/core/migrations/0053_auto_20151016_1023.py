# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_auto_20151013_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='prefix',
            field=models.CharField(help_text=b'A prefix like "The" that shouldn\'t be used for searching', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='subtitle',
            field=models.CharField(help_text=b'Subtitle of the book.', max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(help_text=b'The main title.', max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/Users/andy/Code/rua/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
        ),
    ]
