# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150826_0909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalformelementsrelationship',
            name='element_class',
        ),
        migrations.AddField(
            model_name='proposalformelementsrelationship',
            name='width',
            field=models.CharField(blank=True, max_length=20, null=True, help_text=b'Vertical Space taken by the element when rendering the form', choices=[(b'col-md-4', b'third'), (b'col-md-6', b'half'), (b'col-md-12', b'full')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/mauro/Projects/rua/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
        ),
    ]
