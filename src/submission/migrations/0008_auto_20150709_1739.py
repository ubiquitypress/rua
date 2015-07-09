# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_remove_formresult_review_assignment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0047_auto_20150709_1611'),
        ('submission', '0007_proposal_date_submitted'),
    ]

    operations = [
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
                ('competing_interests', models.TextField(help_text=b"If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'", null=True, blank=True)),
                ('files', models.ManyToManyField(to='core.File', null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='proposal',
            name='date_review_started',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='review_form',
            field=models.ForeignKey(blank=True, to='review.Form', null=True),
        ),
        migrations.AddField(
            model_name='proposalreview',
            name='proposal',
            field=models.ForeignKey(to='submission.Proposal'),
        ),
        migrations.AddField(
            model_name='proposalreview',
            name='results',
            field=models.ForeignKey(blank=True, to='review.FormResult', null=True),
        ),
        migrations.AddField(
            model_name='proposalreview',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposal',
            name='review_assignments',
            field=models.ManyToManyField(related_name='review', null=True, to='submission.ProposalReview', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='proposalreview',
            unique_together=set([('proposal', 'user')]),
        ),
    ]
