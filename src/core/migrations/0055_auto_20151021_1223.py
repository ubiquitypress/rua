# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20151019_0852'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhysicalFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('sequence', models.IntegerField(default=999)),
                ('file_type', models.CharField(max_length=100, choices=[(b'hardback', b'Hardback'), (b'paperback', b'Paperback')])),
                ('book', models.ForeignKey(to='core.Book')),
            ],
            options={
                'ordering': ('sequence', 'name'),
            },
        ),
        migrations.AddField(
            model_name='chapter',
            name='file_type',
            field=models.CharField(default='HTML', max_length=100, choices=[(b'epub', b'EPUB'), (b'html', b'HTML'), (b'kindle', b'Kindle'), (b'mobi', b'MOBI'), (b'pdf', b'PDF'), (b'xml', b'XML')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='format',
            name='file_type',
            field=models.CharField(default='HTML', max_length=100, choices=[(b'epub', b'EPUB'), (b'html', b'HTML'), (b'kindle', b'Kindle'), (b'mobi', b'MOBI'), (b'pdf', b'PDF'), (b'xml', b'XML')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/Users/andy/Code/rua/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
        ),
    ]
