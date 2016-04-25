# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('data', models.TextField()),
                ('date_review_started', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(default=b'submission', max_length=20, choices=[(b'submission', b'Submission'), (b'revisions_required', b'Revisions Required'), (b'revisions_submitted', b'Revisions Submitted'), (b'accepted', b'Accepted'), (b'declined', b'Declined')])),
                ('form', models.ForeignKey(to='core.ProposalForm')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProposalReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assigned', models.DateField(auto_now=True)),
                ('accepted', models.DateField(null=True, blank=True)),
                ('declined', models.DateField(null=True, blank=True)),
                ('due', models.DateField(null=True, blank=True)),
                ('completed', models.DateField(null=True, blank=True)),
                ('recommendation', models.CharField(blank=True, max_length=10, null=True, choices=[(b'accept', b'Accept'), (b'reject', b'Reject'), (b'revisions', b'Revisions Required')])),
                ('competing_interests', models.TextField(help_text=b"If any of the authors or editors have any competing interests please add them here. e.g.. 'This study was paid for by corp xyz.'", null=True, blank=True)),
                ('files', models.ManyToManyField(to='core.File', null=True, blank=True)),
                ('proposal', models.ForeignKey(to='submission.Proposal')),
                ('results', models.ForeignKey(blank=True, to='review.FormResult', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionChecklistItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=500)),
                ('sequence', models.IntegerField(default=999)),
                ('required', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('sequence', 'text'),
            },
        ),
        migrations.AddField(
            model_name='proposal',
            name='review_assignments',
            field=models.ManyToManyField(related_name='review', null=True, to='submission.ProposalReview', blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='review_form',
            field=models.ForeignKey(blank=True, to='review.Form', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='proposalreview',
            unique_together=set([('proposal', 'user')]),
        ),
    ]
