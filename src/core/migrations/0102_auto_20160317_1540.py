# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_auto_20160120_1640'),
        ('core', '0101_auto_20160317_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='editorialreviewassignment',
            old_name='competing_interests',
            new_name='editorial_board_competing_interests',
        ),
        migrations.RenameField(
            model_name='editorialreviewassignment',
            old_name='recommendation',
            new_name='editorial_board_recommendation',
        ),
        migrations.RemoveField(
            model_name='editorialreviewassignment',
            name='results',
        ),
        migrations.AddField(
            model_name='editorialreviewassignment',
            name='editorial_board_results',
            field=models.ForeignKey(related_name='eb_review_form_results', blank=True, to='review.FormResult', null=True),
        ),
        migrations.AddField(
            model_name='editorialreviewassignment',
            name='editorial_board_review_form',
            field=models.ForeignKey(related_name='eb_review_form', blank=True, to='review.Form', null=True),
        ),
        migrations.AddField(
            model_name='editorialreviewassignment',
            name='publication_committee_competing_interests',
            field=models.TextField(help_text=b"If any of the authors or editors have any competing interests please add them here. e.g.. 'This study was paid for by corp xyz.'. <a href='/page/competing_interests/'>More info</a>", null=True, blank=True),
        ),
        migrations.AddField(
            model_name='editorialreviewassignment',
            name='publication_committee_recommendation',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'accept', b'Accept'), (b'reject', b'Reject'), (b'revisions', b'Revisions Required')]),
        ),
        migrations.AddField(
            model_name='editorialreviewassignment',
            name='publication_committee_results',
            field=models.ForeignKey(related_name='pc_review_form_results', blank=True, to='review.FormResult', null=True),
        ),
        migrations.AddField(
            model_name='editorialreviewassignment',
            name='publication_committee_review_form',
            field=models.ForeignKey(related_name='pc_review_form', blank=True, to='review.Form', null=True),
        ),
    ]
