# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20150508_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mime_type', models.CharField(max_length=50)),
                ('original_filename', models.CharField(max_length=1000)),
                ('uuid_filename', models.CharField(max_length=100)),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
                ('stage_uploaded', models.IntegerField()),
                ('kind', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Files',
        ),
        migrations.AlterField(
            model_name='book',
            name='files',
            field=models.ManyToManyField(to='core.File'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/andy/smw/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='stage',
            name='current_stage',
            field=models.CharField(blank=True, max_length=b'20', null=True, choices=[(b'proposal', b'Proposal'), (b'submission', b'New Submission'), (b'i_review', b'Internal Review'), (b'e_review', b'External Review'), (b'copy_editing', b'Copy Editing'), (b'indexing', b'Indexing'), (b'production', b'Production'), (b'published', b'Published')]),
        ),
    ]
