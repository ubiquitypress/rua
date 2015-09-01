# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0011_auto_20150829_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='CopyeditAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.DateTimeField(null=True, blank=True)),
                ('declined', models.DateTimeField(null=True, blank=True)),
                ('due', models.DateTimeField(null=True, blank=True)),
                ('completed', models.DateTimeField(null=True, blank=True)),
                ('book', models.ForeignKey(to='core.Book')),
                ('copyeditor', models.ForeignKey(related_name='copyeditor', to=settings.AUTH_USER_MODEL)),
                ('files', models.ManyToManyField(to='core.File', null=True, blank=True)),
                ('requestor', models.ForeignKey(related_name='copyedit_requestor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IndexAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.DateTimeField(null=True, blank=True)),
                ('declined', models.DateTimeField(null=True, blank=True)),
                ('due', models.DateTimeField(null=True, blank=True)),
                ('completed', models.DateTimeField(null=True, blank=True)),
                ('book', models.ForeignKey(to='core.Book')),
                ('files', models.ManyToManyField(to='core.File', null=True, blank=True)),
                ('indexer', models.ForeignKey(related_name='indexer', to=settings.AUTH_USER_MODEL)),
                ('requestor', models.ForeignKey(related_name='index_requestor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TypesetAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.DateTimeField(null=True, blank=True)),
                ('declined', models.DateTimeField(null=True, blank=True)),
                ('due', models.DateTimeField(null=True, blank=True)),
                ('completed', models.DateTimeField(null=True, blank=True)),
                ('book', models.ForeignKey(to='core.Book')),
                ('files', models.ManyToManyField(to='core.File', null=True, blank=True)),
                ('requestor', models.ForeignKey(related_name='typeset_requestor', to=settings.AUTH_USER_MODEL)),
                ('typesetter', models.ForeignKey(related_name='typesetter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
