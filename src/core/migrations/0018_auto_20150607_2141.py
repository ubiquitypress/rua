# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0017_profile_roles'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('review_type', models.CharField(max_length=15, choices=[(b'internal', b'Internal'), (b'external', b'External')])),
                ('assigned', models.DateField(auto_now=True)),
                ('accepted', models.DateField(null=True, blank=True)),
                ('completed', models.DateField(null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('access_key', models.CharField(max_length=200)),
                ('file', models.ForeignKey(blank=True, to='core.File', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='review_assignments',
            field=models.ManyToManyField(to='core.ReviewAssignment'),
        ),
    ]
