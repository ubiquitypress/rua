# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20150928_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of retailer, eg. Amazon or Book Depository', max_length=300)),
                ('link', models.URLField(help_text=b'FQDN of the book on the retailer website eg. http://www.amazon.co.uk/mybook/', max_length=2000)),
                ('price', models.DecimalField(help_text=b'Decimal value eg. 22.99 or 9.99', max_digits=6, decimal_places=2)),
                ('enabled', models.BooleanField(default=True)),
                ('book', models.ForeignKey(to='core.Book')),
            ],
        ),
        migrations.RemoveField(
            model_name='printsales',
            name='book',
        ),
        migrations.DeleteModel(
            name='PrintSales',
        ),
    ]
