# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150522_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='submission_stage',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_type',
            field=models.CharField(blank=True, max_length=50, null=True, help_text=b'A monograph is a work authored, in its entirety, by one or more authors. An edited volume has different authors for each chapter.', choices=[(b'monograph', b'Monograph'), (b'edited_volume', b'Edited Volume')]),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_letter',
            field=models.TextField(help_text=b'A covering letter for the Editors.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(max_length=5000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='editor',
            field=models.ManyToManyField(to='core.Editor'),
        ),
        migrations.AlterField(
            model_name='book',
            name='license',
            field=models.ForeignKey(blank=True, to='core.License', help_text=b'The license you recommend for this work.', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='prefix',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='series',
            field=models.ForeignKey(blank=True, to='core.Series', help_text=b'If you are submitting this work to an existing Series please selected it.', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
