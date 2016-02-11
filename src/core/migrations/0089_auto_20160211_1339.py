# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0088_setting_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='peer_review_override',
            field=models.BooleanField(default=False, help_text=b'If enabled, this will mark a book as Peer Reviewed even if there is no Reviews in the Rua database.'),
        ),
        migrations.AlterField(
            model_name='book',
            name='competing_interests',
            field=models.TextField(help_text=b"If any there are any competing interests please add them here. EG. 'This study was paid for by corp xyz.'. <a href='/page/competing_interests/'>More info</a>", null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/Users/andy/Code/rua/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
        ),
    ]
