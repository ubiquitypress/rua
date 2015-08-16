# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_auto_20150809_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalFormElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('choices', models.CharField(help_text=b'Seperate choices with the bar | character.', max_length=500, null=True, blank=True)),
                ('field_type', models.CharField(max_length=100, choices=[(b'text', b'Text Field'), (b'textarea', b'Text Area'), (b'check', b'Check Box'), (b'select', b'Select'), (b'email', b'Email'), (b'upload', b'Upload'), (b'date', b'Date')])),
                ('required', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ProposalFormElementsRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('element_class', models.CharField(max_length=20, null=True, blank=True)),
                ('help_text', models.TextField(max_length=1000, null=True, blank=True)),
                ('element', models.ForeignKey(to='core.ProposalFormElement')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.RemoveField(
            model_name='proposalform',
            name='active',
        ),
        migrations.RemoveField(
            model_name='proposalform',
            name='form',
        ),
        migrations.AddField(
            model_name='proposalform',
            name='completion_text',
            field=models.TextField(default=1, help_text=b'Accepts HTML. Para elements should be wrapped in paragraph tags or they will not have fonts.', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposalform',
            name='intro_text',
            field=models.TextField(default=1, help_text=b'Accepts HTML. Para elements should be wrapped in paragraph tags or they will not have fonts.', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposalform',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposalform',
            name='ref',
            field=models.CharField(default=1, help_text=b'for proposals: press_code-proposal eg. sup-proposal', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposalformelementsrelationship',
            name='form',
            field=models.ForeignKey(to='core.ProposalForm'),
        ),
        migrations.AddField(
            model_name='proposalform',
            name='fields',
            field=models.ManyToManyField(to='core.ProposalFormElement', through='core.ProposalFormElementsRelationship'),
        ),
    ]
