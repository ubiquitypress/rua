# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('ref', models.CharField(help_text=b'for proposals: press_code-proposal eg. sup-proposal', max_length=20)),
                ('intro_text', models.TextField(help_text=b'Accepts HTML. Para elements should be wrapped in paragraph tags or they will not have fonts.', max_length=1000)),
                ('completion_text', models.TextField(help_text=b'Accepts HTML. Para elements should be wrapped in paragraph tags or they will not have fonts.', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='FormElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('choices', models.CharField(help_text=b'Seperate choices with the bar | character.', max_length=500, null=True, blank=True)),
                ('field_type', models.CharField(max_length=100, choices=[(b'text', b'Text Field'), (b'textarea', b'Text Area'), (b'check', b'Check Box'), (b'select', b'Select'), (b'email', b'Email'), (b'upload', b'Upload'), (b'date', b'Date')])),
                ('required', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='FormElementsRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('element_class', models.CharField(max_length=20, null=True, blank=True)),
                ('help_text', models.TextField(max_length=1000, null=True, blank=True)),
                ('element', models.ForeignKey(to='review.FormElement')),
                ('form', models.ForeignKey(to='review.Form')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='FormResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('form', models.ForeignKey(to='review.Form')),
            ],
        ),
        migrations.AddField(
            model_name='form',
            name='fields',
            field=models.ManyToManyField(to='review.FormElement', through='review.FormElementsRelationship'),
        ),
    ]
