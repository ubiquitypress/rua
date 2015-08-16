# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
<<<<<<< HEAD
import django.core.files.storage
import core.models
=======
>>>>>>> a9374d5a87f61bd9eb8bc886509b518ec8833ba5


class Migration(migrations.Migration):

    dependencies = [
<<<<<<< HEAD
        ('review', '0005_remove_formresult_review_assignment'),
=======
>>>>>>> a9374d5a87f61bd9eb8bc886509b518ec8833ba5
        ('core', '0051_auto_20150804_2254'),
    ]

    operations = [
<<<<<<< HEAD
        migrations.CreateModel(
            name='ProposalForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False)),
                ('form', models.ForeignKey(to='review.Form')),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/mauro/Projects/rua/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True),
=======
        migrations.RemoveField(
            model_name='contract',
            name='file',
        ),
        migrations.AddField(
            model_name='contract',
            name='author_file',
            field=models.ForeignKey(related_name='author_file', default=1, to='core.File'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='editor_file',
            field=models.ForeignKey(related_name='editor_file', blank=True, to='core.File', null=True),
>>>>>>> a9374d5a87f61bd9eb8bc886509b518ec8833ba5
        ),
    ]
