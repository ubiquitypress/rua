# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150522_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='sequence',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(to='core.Author', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(max_length=5000, null=True, verbose_name=b'Abstract', blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='editor',
            field=models.ManyToManyField(to='core.Editor', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='files',
            field=models.ManyToManyField(to='core.File', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='keywords',
            field=models.ManyToManyField(to='core.Keyword', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='subject',
            field=models.ManyToManyField(to='core.Subject', null=True, blank=True),
        ),
    ]
