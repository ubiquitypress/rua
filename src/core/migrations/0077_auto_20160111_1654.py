# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0076_profile_reset_code_validated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/Users/ioanniscleary/Code/rua/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='interest',
            field=models.ManyToManyField(to='core.Interest', null=True, blank=True),
        ),
    ]
