# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0006_auto_20160120_1640'),
        ('core', '0100_auto_20160317_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditorialReviewAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assigned', models.DateField(auto_now=True)),
                ('accepted', models.DateField(null=True, blank=True)),
                ('declined', models.DateField(null=True, blank=True)),
                ('due', models.DateField(null=True, blank=True)),
                ('completed', models.DateField(null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('editorial_board_access_key', models.CharField(max_length=258, null=True, blank=True)),
                ('publishing_committee_access_key', models.CharField(max_length=258, null=True, blank=True)),
                ('editorial_board_passed', models.BooleanField(default=False)),
                ('publication_committee_passed', models.BooleanField(default=False)),
                ('recommendation', models.CharField(blank=True, max_length=10, null=True, choices=[(b'accept', b'Accept'), (b'reject', b'Reject'), (b'revisions', b'Revisions Required')])),
                ('competing_interests', models.TextField(help_text=b"If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'. <a href='/page/competing_interests/'>More info</a>", null=True, blank=True)),
                ('unaccepted_reminder', models.BooleanField(default=False)),
                ('accepted_reminder', models.BooleanField(default=False)),
                ('overdue_reminder', models.BooleanField(default=False)),
                ('reopened', models.BooleanField(default=False)),
                ('withdrawn', models.BooleanField(default=False)),
                ('book', models.ForeignKey(to='core.Book')),
                ('editorial_board', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
                ('files', models.ManyToManyField(to='core.File', null=True, blank=True)),
                ('management_editor', models.ForeignKey(related_name='management_editor', to=settings.AUTH_USER_MODEL)),
                ('results', models.ForeignKey(blank=True, to='review.FormResult', null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='bookreviewassignment',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='bookreviewassignment',
            name='book',
        ),
        migrations.RemoveField(
            model_name='bookreviewassignment',
            name='editorial_board',
        ),
        migrations.RemoveField(
            model_name='bookreviewassignment',
            name='files',
        ),
        migrations.RemoveField(
            model_name='bookreviewassignment',
            name='management_editor',
        ),
        migrations.RemoveField(
            model_name='bookreviewassignment',
            name='results',
        ),
        migrations.DeleteModel(
            name='BookReviewAssignment',
        ),
        migrations.AlterUniqueTogether(
            name='editorialreviewassignment',
            unique_together=set([('book', 'management_editor')]),
        ),
    ]
