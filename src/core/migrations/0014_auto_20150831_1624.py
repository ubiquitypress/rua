# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150831_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copyeditassignment',
            name='accepted',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='copyeditassignment',
            name='completed',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='copyeditassignment',
            name='declined',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='copyeditassignment',
            name='due',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='copyeditassignment',
            name='requested',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='indexassignment',
            name='accepted',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='indexassignment',
            name='completed',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='indexassignment',
            name='declined',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='indexassignment',
            name='due',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='indexassignment',
            name='requested',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='typesetassignment',
            name='accepted',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='typesetassignment',
            name='completed',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='typesetassignment',
            name='declined',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='typesetassignment',
            name='due',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='typesetassignment',
            name='requested',
            field=models.DateField(auto_now_add=True),
        ),
    ]
