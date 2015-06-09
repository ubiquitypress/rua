# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_book_review_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='book',
            field=models.ForeignKey(default=1, to='core.Book'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='review_assignments',
            field=models.ManyToManyField(related_name='review', to='core.ReviewAssignment'),
        ),
        migrations.AlterUniqueTogether(
            name='reviewassignment',
            unique_together=set([('book', 'user')]),
        ),
    ]
