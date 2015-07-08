# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_reviewassignment_competing_interests'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewRound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_number', models.IntegerField()),
                ('book', models.ForeignKey(to='core.Book')),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/mauro/Code/smw/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='reviewassignment',
            name='competing_interests',
            field=models.TextField(help_text=b"If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'", null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='reviewround',
            unique_together=set([('book', 'round_number')]),
        ),
    ]
