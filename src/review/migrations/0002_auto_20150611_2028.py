# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_reviewassignment_form'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(default=b'new', max_length=20, null=True, blank=True, choices=[(b'new', b'New'), (b'accepted', b'Accepted'), (b'rejected', b'Rejected'), (b'revisions', b'Revisions Required')])),
                ('form', models.ForeignKey(to='review.Form')),
                ('review_assignment', models.ForeignKey(to='core.ReviewAssignment')),
            ],
        ),
        migrations.RemoveField(
            model_name='formresults',
            name='form',
        ),
        migrations.RemoveField(
            model_name='formresults',
            name='review_assignment',
        ),
        migrations.DeleteModel(
            name='FormResults',
        ),
    ]
