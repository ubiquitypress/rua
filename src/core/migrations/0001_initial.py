# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import django.core.files.storage
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100)),
                ('salutation', models.CharField(blank=True, max_length=10, null=True, choices=[(b'Miss', b'Miss'), (b'Ms', b'Ms'), (b'Mrs', b'Mrs'), (b'Mr', b'Mr'), (b'Dr', b'Dr'), (b'Prof.', b'Prof.')])),
                ('institution', models.CharField(max_length=1000)),
                ('department', models.CharField(max_length=300, null=True, blank=True)),
                ('country', models.CharField(max_length=300, choices=[(b'', b'Countries...'), ('AF', 'Afghanistan'), ('AX', '\xc5land Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia, Plurinational State of'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, The Democratic Republic of the'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "C\xf4te d'Ivoire"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Cura\xe7ao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See (Vatican City State)'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran, Islamic Republic of'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea, Democratic People's Republic of"), ('KR', 'Korea, Republic of'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MK', 'Macedonia, Republic of'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia, Federated States of'), ('MD', 'Moldova, Republic of'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine, State of'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'R\xe9union'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint Barth\xe9lemy'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten (Dutch part)'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SS', 'South Sudan'), ('SJ', 'Svalbard and Jan Mayen'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan, Province of China'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela, Bolivarian Republic of'), ('VN', 'Viet Nam'), ('VG', 'Virgin Islands, British'), ('VI', 'Virgin Islands, U.S.'), ('WF', 'Wallis and Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')])),
                ('author_email', models.CharField(max_length=100)),
                ('biography', models.TextField(max_length=3000, null=True, blank=True)),
                ('orcid', models.CharField(max_length=40, null=True, verbose_name=b'ORCiD', blank=True)),
                ('twitter', models.CharField(max_length=300, null=True, verbose_name=b'Twitter Handle', blank=True)),
                ('linkedin', models.CharField(max_length=300, null=True, verbose_name=b'Linkedin Profile', blank=True)),
                ('facebook', models.CharField(max_length=300, null=True, verbose_name=b'Facebook Profile', blank=True)),
                ('sequence', models.IntegerField(default=1, null=True, blank=True)),
            ],
            options={
                'ordering': ('sequence',),
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prefix', models.CharField(max_length=100, null=True, blank=True)),
                ('title', models.CharField(max_length=1000, null=True, blank=True)),
                ('subtitle', models.CharField(max_length=1000, null=True, blank=True)),
                ('description', models.TextField(max_length=5000, null=True, verbose_name=b'Abstract', blank=True)),
                ('cover', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('doi', models.CharField(max_length=25, null=True, blank=True)),
                ('pages', models.CharField(max_length=10, null=True, blank=True)),
                ('slug', models.CharField(max_length=1000, null=True, blank=True)),
                ('cover_letter', models.TextField(help_text=b'A covering letter for the Editors.', null=True, blank=True)),
                ('reviewer_suggestions', models.TextField(null=True, blank=True)),
                ('competing_interests', models.TextField(help_text=b"If any of the authors or editors have any competing interests please add them here. e.g.. 'This study was paid for by corp xyz.'", null=True, blank=True)),
                ('book_type', models.CharField(blank=True, max_length=50, null=True, help_text=b'A monograph is a work authored, in its entirety, by one or more authors. An edited volume has different authors for each chapter.', choices=[(b'monograph', b'Monograph'), (b'edited_volume', b'Edited Volume')])),
                ('submission_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('publicaton_date', models.DateTimeField(null=True, blank=True)),
                ('submission_stage', models.IntegerField(null=True, blank=True)),
                ('author', models.ManyToManyField(to='core.Author', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('identifier', models.CharField(unique=True, max_length=200)),
                ('sequence', models.IntegerField(default=9999)),
                ('book', models.ForeignKey(to='core.Book')),
            ],
            options={
                'ordering': ('sequence', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1000)),
                ('notes', models.TextField(null=True, blank=True)),
                ('editor_signed_off', models.DateField(null=True, blank=True)),
                ('author_signed_off', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100)),
                ('salutation', models.CharField(blank=True, max_length=10, null=True, choices=[(b'Miss', b'Miss'), (b'Ms', b'Ms'), (b'Mrs', b'Mrs'), (b'Mr', b'Mr'), (b'Dr', b'Dr'), (b'Prof.', b'Prof.')])),
                ('institution', models.CharField(max_length=1000)),
                ('department', models.CharField(max_length=300, null=True, blank=True)),
                ('country', models.CharField(max_length=300, choices=[(b'', b'Countries...'), ('AF', 'Afghanistan'), ('AX', '\xc5land Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia, Plurinational State of'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, The Democratic Republic of the'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "C\xf4te d'Ivoire"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Cura\xe7ao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See (Vatican City State)'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran, Islamic Republic of'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea, Democratic People's Republic of"), ('KR', 'Korea, Republic of'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MK', 'Macedonia, Republic of'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia, Federated States of'), ('MD', 'Moldova, Republic of'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine, State of'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'R\xe9union'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint Barth\xe9lemy'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten (Dutch part)'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SS', 'South Sudan'), ('SJ', 'Svalbard and Jan Mayen'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan, Province of China'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela, Bolivarian Republic of'), ('VN', 'Viet Nam'), ('VG', 'Virgin Islands, British'), ('VI', 'Virgin Islands, U.S.'), ('WF', 'Wallis and Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')])),
                ('author_email', models.CharField(max_length=100)),
                ('biography', models.TextField(max_length=3000, null=True, blank=True)),
                ('orcid', models.CharField(max_length=40, null=True, verbose_name=b'ORCiD', blank=True)),
                ('twitter', models.CharField(max_length=300, null=True, verbose_name=b'Twitter Handle', blank=True)),
                ('linkedin', models.CharField(max_length=300, null=True, verbose_name=b'Linkedin Profile', blank=True)),
                ('facebook', models.CharField(max_length=300, null=True, verbose_name=b'Facebook Profile', blank=True)),
                ('sequence', models.IntegerField(default=1, null=True, blank=True)),
            ],
            options={
                'ordering': ('sequence',),
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mime_type', models.CharField(max_length=50)),
                ('original_filename', models.CharField(max_length=1000)),
                ('uuid_filename', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=200, null=True, blank=True)),
                ('description', models.CharField(max_length=1000, null=True, blank=True)),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
                ('stage_uploaded', models.IntegerField()),
                ('kind', models.CharField(max_length=100)),
                ('sequence', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ('sequence', '-kind'),
            },
        ),
        migrations.CreateModel(
            name='FileVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_filename', models.CharField(max_length=1000)),
                ('uuid_filename', models.CharField(max_length=100)),
                ('date_uploaded', models.DateTimeField()),
                ('file', models.ForeignKey(to='core.File')),
            ],
            options={
                'ordering': ('-date_uploaded',),
            },
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('identifier', models.CharField(unique=True, max_length=200)),
                ('sequence', models.IntegerField(default=9999)),
                ('book', models.ForeignKey(to='core.Book')),
                ('file', models.ForeignKey(to='core.File')),
            ],
            options={
                'ordering': ('sequence', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1000)),
                ('short_name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('version', models.CharField(max_length=10)),
                ('url', models.URLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=100, choices=[(b'submission', b'Submission'), (b'workflow', b'Workflow'), (b'file', b'File')])),
                ('short_name', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('date_logged', models.DateTimeField(auto_now_add=True, null=True)),
                ('book', models.ForeignKey(to='core.Book')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_code', models.CharField(max_length=100, null=True, blank=True)),
                ('salutation', models.CharField(blank=True, max_length=10, null=True, choices=[(b'Miss', b'Miss'), (b'Ms', b'Ms'), (b'Mrs', b'Mrs'), (b'Mr', b'Mr'), (b'Dr', b'Dr'), (b'Prof.', b'Prof.')])),
                ('middle_name', models.CharField(max_length=300, null=True, blank=True)),
                ('biography', models.TextField(null=True, blank=True)),
                ('orcid', models.CharField(max_length=40, null=True, verbose_name=b'ORCiD', blank=True)),
                ('institution', models.CharField(max_length=1000)),
                ('department', models.CharField(max_length=300, null=True, blank=True)),
                ('country', models.CharField(max_length=300, choices=[(b'', b'Countries...'), ('AF', 'Afghanistan'), ('AX', '\xc5land Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia, Plurinational State of'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, The Democratic Republic of the'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "C\xf4te d'Ivoire"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Cura\xe7ao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See (Vatican City State)'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran, Islamic Republic of'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea, Democratic People's Republic of"), ('KR', 'Korea, Republic of'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MK', 'Macedonia, Republic of'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia, Federated States of'), ('MD', 'Moldova, Republic of'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine, State of'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'R\xe9union'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint Barth\xe9lemy'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten (Dutch part)'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SS', 'South Sudan'), ('SJ', 'Svalbard and Jan Mayen'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan, Province of China'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela, Bolivarian Republic of'), ('VN', 'Viet Nam'), ('VG', 'Virgin Islands, British'), ('VI', 'Virgin Islands, U.S.'), ('WF', 'Wallis and Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')])),
                ('twitter', models.CharField(max_length=300, null=True, verbose_name=b'Twitter Handle', blank=True)),
                ('facebook', models.CharField(max_length=300, null=True, verbose_name=b'Facebook Handle', blank=True)),
                ('linkedin', models.CharField(max_length=300, null=True, verbose_name=b'Linkedin Profile', blank=True)),
                ('impactstory', models.CharField(max_length=300, null=True, verbose_name=b'ImpactStory ID', blank=True)),
                ('github', models.CharField(max_length=300, null=True, verbose_name=b'Github Username', blank=True)),
                ('profile_image', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/mauro/Projects/rua/src/media'), null=True, upload_to=core.models.profile_images_upload_path, blank=True)),
                ('email_sent', models.DateTimeField(null=True, blank=True)),
                ('date_confirmed', models.DateTimeField(null=True, blank=True)),
                ('confirmation_code', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProposalForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('ref', models.CharField(help_text=b'for proposals: press_code-proposal eg. sup-proposal', max_length=20)),
                ('intro_text', models.TextField(help_text=b'Accepts HTML. Para elements should be wrapped in paragraph tags or they will not have fonts.', max_length=1000)),
                ('completion_text', models.TextField(help_text=b'Accepts HTML. Para elements should be wrapped in paragraph tags or they will not have fonts.', max_length=1000)),
            ],
        ),
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
                ('form', models.ForeignKey(to='core.ProposalForm')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='ReviewAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('review_type', models.CharField(max_length=15, choices=[(b'internal', b'Internal'), (b'external', b'External')])),
                ('assigned', models.DateField(auto_now=True)),
                ('accepted', models.DateField(null=True, blank=True)),
                ('declined', models.DateField(null=True, blank=True)),
                ('due', models.DateField(null=True, blank=True)),
                ('completed', models.DateField(null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('access_key', models.CharField(max_length=200)),
                ('recommendation', models.CharField(blank=True, max_length=10, null=True, choices=[(b'accept', b'Accept'), (b'reject', b'Reject'), (b'revisions', b'Revisions Required')])),
                ('competing_interests', models.TextField(help_text=b"If any of the authors or editors have any competing interests please add them here. e.g.. 'This study was paid for by corp xyz.'", null=True, blank=True)),
                ('unaccepted_reminder', models.BooleanField(default=False)),
                ('accepted_reminder', models.BooleanField(default=False)),
                ('overdue_reminder', models.BooleanField(default=False)),
                ('book', models.ForeignKey(to='core.Book')),
                ('files', models.ManyToManyField(to='core.File', null=True, blank=True)),
                ('results', models.ForeignKey(blank=True, to='review.FormResult', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewRound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_number', models.IntegerField()),
                ('book', models.ForeignKey(to='core.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('issn', models.CharField(max_length=15)),
                ('description', models.TextField(null=True, blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('editor', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('types', models.CharField(max_length=20, choices=[(b'rich_text', b'Rich Text'), (b'text', b'Text'), (b'char', b'Characters'), (b'number', b'Number'), (b'boolean', b'Boolean'), (b'file', b'File')])),
                ('value', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('group', 'name'),
            },
        ),
        migrations.CreateModel(
            name='SettingGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_stage', models.CharField(blank=True, max_length=b'20', null=True, choices=[(b'proposal', b'Proposal'), (b'submission', b'New Submission'), (b'review', b'Review'), (b'editing', b'Editing'), (b'production', b'Production'), (b'published', b'Published'), (b'declined', b'Declined')])),
                ('proposal', models.DateTimeField(null=True, blank=True)),
                ('submission', models.DateTimeField(null=True, blank=True)),
                ('review', models.DateTimeField(null=True, blank=True)),
                ('internal_review', models.DateTimeField(null=True, blank=True)),
                ('external_review', models.DateTimeField(null=True, blank=True)),
                ('editing', models.DateTimeField(null=True, blank=True)),
                ('production', models.DateTimeField(null=True, blank=True)),
                ('publication', models.DateTimeField(null=True, blank=True)),
                ('declined', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('workflow', models.CharField(max_length=50, choices=[(b'submission', b'Submission'), (b'review', b'Review'), (b'editing', b'Editing'), (b'production', b'Production'), (b'personal', b'Personal')])),
                ('assigned', models.DateField(auto_now_add=True, null=True)),
                ('due', models.DateField(null=True, blank=True)),
                ('completed', models.DateField(null=True, blank=True)),
                ('assignee', models.ForeignKey(related_name='assignee', to=settings.AUTH_USER_MODEL)),
                ('book', models.ForeignKey(blank=True, to='core.Book', null=True)),
                ('creator', models.ForeignKey(related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='setting',
            name='group',
            field=models.ForeignKey(to='core.SettingGroup'),
        ),
        migrations.AddField(
            model_name='reviewassignment',
            name='review_round',
            field=models.ForeignKey(blank=True, to='core.ReviewRound', null=True),
        ),
        migrations.AddField(
            model_name='reviewassignment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposalform',
            name='fields',
            field=models.ManyToManyField(to='core.ProposalFormElement', through='core.ProposalFormElementsRelationship'),
        ),
        migrations.AddField(
            model_name='profile',
            name='roles',
            field=models.ManyToManyField(to='core.Role'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='author_file',
            field=models.ForeignKey(related_name='author_file', blank=True, to='core.File', null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='editor_file',
            field=models.ForeignKey(related_name='editor_file', blank=True, to='core.File', null=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='file',
            field=models.ForeignKey(to='core.File'),
        ),
        migrations.AddField(
            model_name='book',
            name='contract',
            field=models.ForeignKey(blank=True, to='core.Contract', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='editor',
            field=models.ManyToManyField(to='core.Editor', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='external_review_files',
            field=models.ManyToManyField(related_name='external_review_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='files',
            field=models.ManyToManyField(to='core.File', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='internal_review_files',
            field=models.ManyToManyField(related_name='internal_review_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='keywords',
            field=models.ManyToManyField(to='core.Keyword', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='license',
            field=models.ForeignKey(blank=True, to='core.License', help_text=b'The license you recommend for this work.', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='misc_files',
            field=models.ManyToManyField(related_name='misc_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='review_assignments',
            field=models.ManyToManyField(related_name='review', null=True, to='core.ReviewAssignment', blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='review_form',
            field=models.ForeignKey(blank=True, to='review.Form', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='series',
            field=models.ForeignKey(blank=True, to='core.Series', help_text=b'If you are submitting this work to an existing Series please selected it.', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='stage',
            field=models.ForeignKey(blank=True, to='core.Stage', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='subject',
            field=models.ManyToManyField(to='core.Subject', null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='reviewround',
            unique_together=set([('book', 'round_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='reviewassignment',
            unique_together=set([('book', 'user', 'review_type', 'review_round')]),
        ),
    ]
