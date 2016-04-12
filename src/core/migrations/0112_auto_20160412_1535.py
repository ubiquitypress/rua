# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0111_auto_20160324_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChapterFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('identifier', models.CharField(unique=True, max_length=200)),
                ('sequence', models.IntegerField(default=999)),
                ('file_type', models.CharField(max_length=100, choices=[(b'epub', b'EPUB'), (b'html', b'HTML'), (b'kindle', b'Kindle'), (b'mobi', b'MOBI'), (b'pdf', b'PDF'), (b'xml', b'XML')])),
            ],
            options={
                'ordering': ('sequence', 'name'),
            },
        ),
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ('sequence',)},
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='file',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='file_type',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='identifier',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='name',
        ),
        migrations.AddField(
            model_name='book',
            name='table_contents',
            field=models.CharField(default=datetime.datetime(2016, 4, 12, 15, 35, 21, 942760, tzinfo=utc), max_length=100, choices=[(b'book-level', b'Book Level'), (b'chapter-level', b'Chapter Level')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chapter',
            name='blurbs',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='disciplines',
            field=models.ManyToManyField(to='core.Subject', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='keywords',
            field=models.ManyToManyField(to='core.Keyword', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='chapterformat',
            name='book',
            field=models.ForeignKey(to='core.Book'),
        ),
        migrations.AddField(
            model_name='chapterformat',
            name='chapter',
            field=models.ForeignKey(related_name='format_chapter', to='core.Chapter'),
        ),
        migrations.AddField(
            model_name='chapterformat',
            name='file',
            field=models.ForeignKey(to='core.File'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='formats',
            field=models.ManyToManyField(related_name='formats', null=True, to='core.ChapterFormat', blank=True),
        ),
    ]
