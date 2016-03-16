# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0006_auto_20160120_1640'),
        ('core', '0099_reviewassignment_withdrawn'),
        ('submission', '0014_proposalreview_withdrawn'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncompleteProposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name=b'Book Title', blank=True)),
                ('subtitle', models.CharField(max_length=255, null=True, blank=True)),
                ('author', models.CharField(max_length=255, null=True, verbose_name=b'Submitting author/editor', blank=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True, null=True)),
                ('data', models.TextField(null=True, blank=True)),
                ('date_review_started', models.DateTimeField(null=True, blank=True)),
                ('revision_due_date', models.DateTimeField(null=True, blank=True)),
                ('date_accepted', models.DateTimeField(null=True, blank=True)),
                ('book_type', models.CharField(blank=True, max_length=50, null=True, help_text=b'A monograph is a work authored, in its entirety, by one or more authors. An edited volume has different authors for each chapter.', choices=[(b'monograph', b'Monograph'), (b'edited_volume', b'Edited Volume')])),
                ('status', models.CharField(default=b'submission', max_length=20, null=True, blank=True, choices=[(b'submission', b'Submission'), (b'revisions_required', b'Revisions Required'), (b'revisions_submitted', b'Revisions Submitted'), (b'accepted', b'Accepted'), (b'declined', b'Declined')])),
                ('form', models.ForeignKey(blank=True, to='core.ProposalForm', null=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('requestor', models.ForeignKey(related_name='incomplete_editor_requestor', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('review_assignments', models.ManyToManyField(related_name='incomplete_review', null=True, to='submission.ProposalReview', blank=True)),
                ('review_form', models.ForeignKey(blank=True, to='review.Form', null=True)),
            ],
        ),
    ]
