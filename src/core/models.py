from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User

import uuid
import os

from autoslug import AutoSlugField

fs = FileSystemStorage(location=settings.MEDIA_ROOT)

SALUTATION_CHOICES = (
	('Miss', 'Miss'),
	('Ms', 'Ms'),
	('Mrs', 'Mrs'),
	('Mr', 'Mr'),
	('Dr', 'Dr'),
	('Prof.', 'Prof.'),
)

COUNTRY_CHOICES = [('', 'Countries...'), (u'AF', u'Afghanistan'), (u'AX', u'\xc5land Islands'), (u'AL', u'Albania'), (u'DZ', u'Algeria'), (u'AS', u'American Samoa'), (u'AD', u'Andorra'), (u'AO', u'Angola'), (u'AI', u'Anguilla'), (u'AQ', u'Antarctica'), (u'AG', u'Antigua and Barbuda'), (u'AR', u'Argentina'), (u'AM', u'Armenia'), (u'AW', u'Aruba'), (u'AU', u'Australia'), (u'AT', u'Austria'), (u'AZ', u'Azerbaijan'), (u'BS', u'Bahamas'), (u'BH', u'Bahrain'), (u'BD', u'Bangladesh'), (u'BB', u'Barbados'), (u'BY', u'Belarus'), (u'BE', u'Belgium'), (u'BZ', u'Belize'), (u'BJ', u'Benin'), (u'BM', u'Bermuda'), (u'BT', u'Bhutan'), (u'BO', u'Bolivia, Plurinational State of'), (u'BQ', u'Bonaire, Sint Eustatius and Saba'), (u'BA', u'Bosnia and Herzegovina'), (u'BW', u'Botswana'), (u'BV', u'Bouvet Island'), (u'BR', u'Brazil'), (u'IO', u'British Indian Ocean Territory'), (u'BN', u'Brunei Darussalam'), (u'BG', u'Bulgaria'), (u'BF', u'Burkina Faso'), (u'BI', u'Burundi'), (u'KH', u'Cambodia'), (u'CM', u'Cameroon'), (u'CA', u'Canada'), (u'CV', u'Cape Verde'), (u'KY', u'Cayman Islands'), (u'CF', u'Central African Republic'), (u'TD', u'Chad'), (u'CL', u'Chile'), (u'CN', u'China'), (u'CX', u'Christmas Island'), (u'CC', u'Cocos (Keeling) Islands'), (u'CO', u'Colombia'), (u'KM', u'Comoros'), (u'CG', u'Congo'), (u'CD', u'Congo, The Democratic Republic of the'), (u'CK', u'Cook Islands'), (u'CR', u'Costa Rica'), (u'CI', u"C\xf4te d'Ivoire"), (u'HR', u'Croatia'), (u'CU', u'Cuba'), (u'CW', u'Cura\xe7ao'), (u'CY', u'Cyprus'), (u'CZ', u'Czech Republic'), (u'DK', u'Denmark'), (u'DJ', u'Djibouti'), (u'DM', u'Dominica'), (u'DO', u'Dominican Republic'), (u'EC', u'Ecuador'), (u'EG', u'Egypt'), (u'SV', u'El Salvador'), (u'GQ', u'Equatorial Guinea'), (u'ER', u'Eritrea'), (u'EE', u'Estonia'), (u'ET', u'Ethiopia'), (u'FK', u'Falkland Islands (Malvinas)'), (u'FO', u'Faroe Islands'), (u'FJ', u'Fiji'), (u'FI', u'Finland'), (u'FR', u'France'), (u'GF', u'French Guiana'), (u'PF', u'French Polynesia'), (u'TF', u'French Southern Territories'), (u'GA', u'Gabon'), (u'GM', u'Gambia'), (u'GE', u'Georgia'), (u'DE', u'Germany'), (u'GH', u'Ghana'), (u'GI', u'Gibraltar'), (u'GR', u'Greece'), (u'GL', u'Greenland'), (u'GD', u'Grenada'), (u'GP', u'Guadeloupe'), (u'GU', u'Guam'), (u'GT', u'Guatemala'), (u'GG', u'Guernsey'), (u'GN', u'Guinea'), (u'GW', u'Guinea-Bissau'), (u'GY', u'Guyana'), (u'HT', u'Haiti'), (u'HM', u'Heard Island and McDonald Islands'), (u'VA', u'Holy See (Vatican City State)'), (u'HN', u'Honduras'), (u'HK', u'Hong Kong'), (u'HU', u'Hungary'), (u'IS', u'Iceland'), (u'IN', u'India'), (u'ID', u'Indonesia'), (u'IR', u'Iran, Islamic Republic of'), (u'IQ', u'Iraq'), (u'IE', u'Ireland'), (u'IM', u'Isle of Man'), (u'IL', u'Israel'), (u'IT', u'Italy'), (u'JM', u'Jamaica'), (u'JP', u'Japan'), (u'JE', u'Jersey'), (u'JO', u'Jordan'), (u'KZ', u'Kazakhstan'), (u'KE', u'Kenya'), (u'KI', u'Kiribati'), (u'KP', u"Korea, Democratic People's Republic of"), (u'KR', u'Korea, Republic of'), (u'KW', u'Kuwait'), (u'KG', u'Kyrgyzstan'), (u'LA', u"Lao People's Democratic Republic"), (u'LV', u'Latvia'), (u'LB', u'Lebanon'), (u'LS', u'Lesotho'), (u'LR', u'Liberia'), (u'LY', u'Libya'), (u'LI', u'Liechtenstein'), (u'LT', u'Lithuania'), (u'LU', u'Luxembourg'), (u'MO', u'Macao'), (u'MK', u'Macedonia, Republic of'), (u'MG', u'Madagascar'), (u'MW', u'Malawi'), (u'MY', u'Malaysia'), (u'MV', u'Maldives'), (u'ML', u'Mali'), (u'MT', u'Malta'), (u'MH', u'Marshall Islands'), (u'MQ', u'Martinique'), (u'MR', u'Mauritania'), (u'MU', u'Mauritius'), (u'YT', u'Mayotte'), (u'MX', u'Mexico'), (u'FM', u'Micronesia, Federated States of'), (u'MD', u'Moldova, Republic of'), (u'MC', u'Monaco'), (u'MN', u'Mongolia'), (u'ME', u'Montenegro'), (u'MS', u'Montserrat'), (u'MA', u'Morocco'), (u'MZ', u'Mozambique'), (u'MM', u'Myanmar'), (u'NA', u'Namibia'), (u'NR', u'Nauru'), (u'NP', u'Nepal'), (u'NL', u'Netherlands'), (u'NC', u'New Caledonia'), (u'NZ', u'New Zealand'), (u'NI', u'Nicaragua'), (u'NE', u'Niger'), (u'NG', u'Nigeria'), (u'NU', u'Niue'), (u'NF', u'Norfolk Island'), (u'MP', u'Northern Mariana Islands'), (u'NO', u'Norway'), (u'OM', u'Oman'), (u'PK', u'Pakistan'), (u'PW', u'Palau'), (u'PS', u'Palestine, State of'), (u'PA', u'Panama'), (u'PG', u'Papua New Guinea'), (u'PY', u'Paraguay'), (u'PE', u'Peru'), (u'PH', u'Philippines'), (u'PN', u'Pitcairn'), (u'PL', u'Poland'), (u'PT', u'Portugal'), (u'PR', u'Puerto Rico'), (u'QA', u'Qatar'), (u'RE', u'R\xe9union'), (u'RO', u'Romania'), (u'RU', u'Russian Federation'), (u'RW', u'Rwanda'), (u'BL', u'Saint Barth\xe9lemy'), (u'SH', u'Saint Helena, Ascension and Tristan da Cunha'), (u'KN', u'Saint Kitts and Nevis'), (u'LC', u'Saint Lucia'), (u'MF', u'Saint Martin (French part)'), (u'PM', u'Saint Pierre and Miquelon'), (u'VC', u'Saint Vincent and the Grenadines'), (u'WS', u'Samoa'), (u'SM', u'San Marino'), (u'ST', u'Sao Tome and Principe'), (u'SA', u'Saudi Arabia'), (u'SN', u'Senegal'), (u'RS', u'Serbia'), (u'SC', u'Seychelles'), (u'SL', u'Sierra Leone'), (u'SG', u'Singapore'), (u'SX', u'Sint Maarten (Dutch part)'), (u'SK', u'Slovakia'), (u'SI', u'Slovenia'), (u'SB', u'Solomon Islands'), (u'SO', u'Somalia'), (u'ZA', u'South Africa'), (u'GS', u'South Georgia and the South Sandwich Islands'), (u'ES', u'Spain'), (u'LK', u'Sri Lanka'), (u'SD', u'Sudan'), (u'SR', u'Suriname'), (u'SS', u'South Sudan'), (u'SJ', u'Svalbard and Jan Mayen'), (u'SZ', u'Swaziland'), (u'SE', u'Sweden'), (u'CH', u'Switzerland'), (u'SY', u'Syrian Arab Republic'), (u'TW', u'Taiwan, Province of China'), (u'TJ', u'Tajikistan'), (u'TZ', u'Tanzania, United Republic of'), (u'TH', u'Thailand'), (u'TL', u'Timor-Leste'), (u'TG', u'Togo'), (u'TK', u'Tokelau'), (u'TO', u'Tonga'), (u'TT', u'Trinidad and Tobago'), (u'TN', u'Tunisia'), (u'TR', u'Turkey'), (u'TM', u'Turkmenistan'), (u'TC', u'Turks and Caicos Islands'), (u'TV', u'Tuvalu'), (u'UG', u'Uganda'), (u'UA', u'Ukraine'), (u'AE', u'United Arab Emirates'), (u'GB', u'United Kingdom'), (u'US', u'United States'), (u'UM', u'United States Minor Outlying Islands'), (u'UY', u'Uruguay'), (u'UZ', u'Uzbekistan'), (u'VU', u'Vanuatu'), (u'VE', u'Venezuela, Bolivarian Republic of'), (u'VN', u'Viet Nam'), (u'VG', u'Virgin Islands, British'), (u'VI', u'Virgin Islands, U.S.'), (u'WF', u'Wallis and Futuna'), (u'EH', u'Western Sahara'), (u'YE', u'Yemen'), (u'ZM', u'Zambia'), (u'ZW', u'Zimbabwe')]
LANGUAGE_CHOICES = ((u'abk', u'Abkhazian'), (u'ace', u'Achinese'), (u'ach', u'Acoli'), (u'ada', u'Adangme'), (u'ady', u'Adyghe; Adygei'), (u'aar', u'Afar'), (u'afh', u'Afrihili'), (u'afr', u'Afrikaans'), (u'afa', u'Afro-Asiatic languages'), (u'ain', u'Ainu'), (u'aka', u'Akan'), (u'akk', u'Akkadian'), (u'sqi', u'Albanian'), (u'ale', u'Aleut'), (u'alg', u'Algonquian languages'), (u'tut', u'Altaic languages'), (u'amh', u'Amharic'), (u'anp', u'Angika'), (u'apa', u'Apache languages'), (u'ara', u'Arabic'), (u'arg', u'Aragonese'), (u'arp', u'Arapaho'), (u'arw', u'Arawak'), (u'hye', u'Armenian'), (u'rup', u'Aromanian; Arumanian; Macedo-Romanian'), (u'art', u'Artificial languages'), (u'asm', u'Assamese'), (u'ast', u'Asturian; Bable; Leonese; Asturleonese'), (u'ath', u'Athapascan languages'), (u'aus', u'Australian languages'), (u'map', u'Austronesian languages'), (u'ava', u'Avaric'), (u'ave', u'Avestan'), (u'awa', u'Awadhi'), (u'aym', u'Aymara'), (u'aze', u'Azerbaijani'), (u'ban', u'Balinese'), (u'bat', u'Baltic languages'), (u'bal', u'Baluchi'), (u'bam', u'Bambara'), (u'bai', u'Bamileke languages'), (u'bad', u'Banda languages'), (u'bnt', u'Bantu languages'), (u'bas', u'Basa'), (u'bak', u'Bashkir'), (u'eus', u'Basque'), (u'btk', u'Batak languages'), (u'bej', u'Beja; Bedawiyet'), (u'bel', u'Belarusian'), (u'bem', u'Bemba'), (u'ben', u'Bengali'), (u'ber', u'Berber languages'), (u'bho', u'Bhojpuri'), (u'bih', u'Bihari languages'), (u'bik', u'Bikol'), (u'bin', u'Bini; Edo'), (u'bis', u'Bislama'), (u'byn', u'Blin; Bilin'), (u'zbl', u'Blissymbols; Blissymbolics; Bliss'), (u'nob', u'Bokm\xe5l, Norwegian; Norwegian Bokm\xe5l'), (u'bos', u'Bosnian'), (u'bra', u'Braj'), (u'bre', u'Breton'), (u'bug', u'Buginese'), (u'bul', u'Bulgarian'), (u'bua', u'Buriat'), (u'mya', u'Burmese'), (u'cad', u'Caddo'), (u'cat', u'Catalan; Valencian'), (u'cau', u'Caucasian languages'), (u'ceb', u'Cebuano'), (u'cel', u'Celtic languages'), (u'cai', u'Central American Indian languages'), (u'khm', u'Central Khmer'), (u'chg', u'Chagatai'), (u'cmc', u'Chamic languages'), (u'cha', u'Chamorro'), (u'che', u'Chechen'), (u'chr', u'Cherokee'), (u'chy', u'Cheyenne'), (u'chb', u'Chibcha'), (u'nya', u'Chichewa; Chewa; Nyanja'), (u'zho', u'Chinese'), (u'chn', u'Chinook jargon'), (u'chp', u'Chipewyan; Dene Suline'), (u'cho', u'Choctaw'), (u'chu', u'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic'), (u'chk', u'Chuukese'), (u'chv', u'Chuvash'), (u'nwc', u'Classical Newari; Old Newari; Classical Nepal Bhasa'), (u'syc', u'Classical Syriac'), (u'cop', u'Coptic'), (u'cor', u'Cornish'), (u'cos', u'Corsican'), (u'cre', u'Cree'), (u'mus', u'Creek'), (u'crp', u'Creoles and pidgins'), (u'cpe', u'Creoles and pidgins, English based'), (u'cpf', u'Creoles and pidgins, French-based'), (u'cpp', u'Creoles and pidgins, Portuguese-based'), (u'crh', u'Crimean Tatar; Crimean Turkish'), (u'hrv', u'Croatian'), (u'cus', u'Cushitic languages'), (u'ces', u'Czech'), (u'dak', u'Dakota'), (u'dan', u'Danish'), (u'dar', u'Dargwa'), (u'del', u'Delaware'), (u'din', u'Dinka'), (u'div', u'Divehi; Dhivehi; Maldivian'), (u'doi', u'Dogri'), (u'dgr', u'Dogrib'), (u'dra', u'Dravidian languages'), (u'dua', u'Duala'), (u'dum', u'Dutch, Middle (ca. 1050-1350)'), (u'nld', u'Dutch; Flemish'), (u'dyu', u'Dyula'), (u'dzo', u'Dzongkha'), (u'frs', u'Eastern Frisian'), (u'efi', u'Efik'), (u'egy', u'Egyptian (Ancient)'), (u'eka', u'Ekajuk'), (u'elx', u'Elamite'), (u'eng', u'English'), (u'enm', u'English, Middle (1100-1500)'), (u'ang', u'English, Old (ca. 450-1100)'), (u'myv', u'Erzya'), (u'epo', u'Esperanto'), (u'est', u'Estonian'), (u'ewe', u'Ewe'), (u'ewo', u'Ewondo'), (u'fan', u'Fang'), (u'fat', u'Fanti'), (u'fao', u'Faroese'), (u'fij', u'Fijian'), (u'fil', u'Filipino; Pilipino'), (u'fin', u'Finnish'), (u'fiu', u'Finno-Ugrian languages'), (u'fon', u'Fon'), (u'fra', u'French'), (u'frm', u'French, Middle (ca. 1400-1600)'), (u'fro', u'French, Old (842-ca. 1400)'), (u'fur', u'Friulian'), (u'ful', u'Fulah'), (u'gaa', u'Ga'), (u'gla', u'Gaelic; Scottish Gaelic'), (u'car', u'Galibi Carib'), (u'glg', u'Galician'), (u'lug', u'Ganda'), (u'gay', u'Gayo'), (u'gba', u'Gbaya'), (u'gez', u'Geez'), (u'kat', u'Georgian'), (u'deu', u'German'), (u'gmh', u'German, Middle High (ca. 1050-1500)'), (u'goh', u'German, Old High (ca. 750-1050)'), (u'gem', u'Germanic languages'), (u'gil', u'Gilbertese'), (u'gon', u'Gondi'), (u'gor', u'Gorontalo'), (u'got', u'Gothic'), (u'grb', u'Grebo'), (u'grc', u'Greek, Ancient (to 1453)'), (u'ell', u'Greek, Modern (1453-)'), (u'grn', u'Guarani'), (u'guj', u'Gujarati'), (u'gwi', u"Gwich'in"), (u'hai', u'Haida'), (u'hat', u'Haitian; Haitian Creole'), (u'hau', u'Hausa'), (u'haw', u'Hawaiian'), (u'heb', u'Hebrew'), (u'her', u'Herero'), (u'hil', u'Hiligaynon'), (u'him', u'Himachali languages; Western Pahari languages'), (u'hin', u'Hindi'), (u'hmo', u'Hiri Motu'), (u'hit', u'Hittite'), (u'hmn', u'Hmong; Mong'), (u'hun', u'Hungarian'), (u'hup', u'Hupa'), (u'iba', u'Iban'), (u'isl', u'Icelandic'), (u'ido', u'Ido'), (u'ibo', u'Igbo'), (u'ijo', u'Ijo languages'), (u'ilo', u'Iloko'), (u'smn', u'Inari Sami'), (u'inc', u'Indic languages'), (u'ine', u'Indo-European languages'), (u'ind', u'Indonesian'), (u'inh', u'Ingush'), (u'ina', u'Interlingua (International Auxiliary Language Association)'), (u'ile', u'Interlingue; Occidental'), (u'iku', u'Inuktitut'), (u'ipk', u'Inupiaq'), (u'ira', u'Iranian languages'), (u'gle', u'Irish'), (u'mga', u'Irish, Middle (900-1200)'), (u'sga', u'Irish, Old (to 900)'), (u'iro', u'Iroquoian languages'), (u'ita', u'Italian'), (u'jpn', u'Japanese'), (u'jav', u'Javanese'), (u'jrb', u'Judeo-Arabic'), (u'jpr', u'Judeo-Persian'), (u'kbd', u'Kabardian'), (u'kab', u'Kabyle'), (u'kac', u'Kachin; Jingpho'), (u'kal', u'Kalaallisut; Greenlandic'), (u'xal', u'Kalmyk; Oirat'), (u'kam', u'Kamba'), (u'kan', u'Kannada'), (u'kau', u'Kanuri'), (u'kaa', u'Kara-Kalpak'), (u'krc', u'Karachay-Balkar'), (u'krl', u'Karelian'), (u'kar', u'Karen languages'), (u'kas', u'Kashmiri'), (u'csb', u'Kashubian'), (u'kaw', u'Kawi'), (u'kaz', u'Kazakh'), (u'kha', u'Khasi'), (u'khi', u'Khoisan languages'), (u'kho', u'Khotanese;Sakan'), (u'kik', u'Kikuyu; Gikuyu'), (u'kmb', u'Kimbundu'), (u'kin', u'Kinyarwanda'), (u'kir', u'Kirghiz; Kyrgyz'), (u'tlh', u'Klingon; tlhIngan-Hol'), (u'kom', u'Komi'), (u'kon', u'Kongo'), (u'kok', u'Konkani'), (u'kor', u'Korean'), (u'kos', u'Kosraean'), (u'kpe', u'Kpelle'), (u'kro', u'Kru languages'), (u'kua', u'Kuanyama; Kwanyama'), (u'kum', u'Kumyk'), (u'kur', u'Kurdish'), (u'kru', u'Kurukh'), (u'kut', u'Kutenai'), (u'lad', u'Ladino'), (u'lah', u'Lahnda'), (u'lam', u'Lamba'), (u'day', u'Land Dayak languages'), (u'lao', u'Lao'), (u'lat', u'Latin'), (u'lav', u'Latvian'), (u'lez', u'Lezghian'), (u'lim', u'Limburgan; Limburger; Limburgish'), (u'lin', u'Lingala'), (u'lit', u'Lithuanian'), (u'jbo', u'Lojban'), (u'nds', u'Low German; Low Saxon; German, Low; Saxon, Low'), (u'dsb', u'Lower Sorbian'), (u'loz', u'Lozi'), (u'lub', u'Luba-Katanga'), (u'lua', u'Luba-Lulua'), (u'lui', u'Luiseno'), (u'smj', u'Lule Sami'), (u'lun', u'Lunda'), (u'luo', u'Luo (Kenya and Tanzania)'), (u'lus', u'Lushai'), (u'ltz', u'Luxembourgish; Letzeburgesch'), (u'mkd', u'Macedonian'), (u'mad', u'Madurese'), (u'mag', u'Magahi'), (u'mai', u'Maithili'), (u'mak', u'Makasar'), (u'mlg', u'Malagasy'), (u'msa', u'Malay'), (u'mal', u'Malayalam'), (u'mlt', u'Maltese'), (u'mnc', u'Manchu'), (u'mdr', u'Mandar'), (u'man', u'Mandingo'), (u'mni', u'Manipuri'), (u'mno', u'Manobo languages'), (u'glv', u'Manx'), (u'mri', u'Maori'), (u'arn', u'Mapudungun; Mapuche'), (u'mar', u'Marathi'), (u'chm', u'Mari'), (u'mah', u'Marshallese'), (u'mwr', u'Marwari'), (u'mas', u'Masai'), (u'myn', u'Mayan languages'), (u'men', u'Mende'), (u'mic', u"Mi'kmaq; Micmac"), (u'min', u'Minangkabau'), (u'mwl', u'Mirandese'), (u'moh', u'Mohawk'), (u'mdf', u'Moksha'), (u'mol', u'Moldavian; Moldovan'), (u'mkh', u'Mon-Khmer languages'), (u'lol', u'Mongo'), (u'mon', u'Mongolian'), (u'mos', u'Mossi'), (u'mul', u'Multiple languages'), (u'mun', u'Munda languages'), (u'nqo', u"N'Ko"), (u'nah', u'Nahuatl languages'), (u'nau', u'Nauru'), (u'nav', u'Navajo; Navaho'), (u'nde', u'Ndebele, North; North Ndebele'), (u'nbl', u'Ndebele, South; South Ndebele'), (u'ndo', u'Ndonga'), (u'nap', u'Neapolitan'), (u'new', u'Nepal Bhasa; Newari'), (u'nep', u'Nepali'), (u'nia', u'Nias'), (u'nic', u'Niger-Kordofanian languages'), (u'ssa', u'Nilo-Saharan languages'), (u'niu', u'Niuean'), (u'zxx', u'No linguistic content; Not applicable'), (u'nog', u'Nogai'), (u'non', u'Norse, Old'), (u'nai', u'North American Indian languages'), (u'frr', u'Northern Frisian'), (u'sme', u'Northern Sami'), (u'nor', u'Norwegian'), (u'nno', u'Norwegian Nynorsk; Nynorsk, Norwegian'), (u'nub', u'Nubian languages'), (u'nym', u'Nyamwezi'), (u'nyn', u'Nyankole'), (u'nyo', u'Nyoro'), (u'nzi', u'Nzima'), (u'oci', u'Occitan (post 1500)'), (u'arc', u'Official Aramaic (700-300 BCE); Imperial Aramaic (700-300 BCE)'), (u'oji', u'Ojibwa'), (u'ori', u'Oriya'), (u'orm', u'Oromo'), (u'osa', u'Osage'), (u'oss', u'Ossetian; Ossetic'), (u'oto', u'Otomian languages'), (u'pal', u'Pahlavi'), (u'pau', u'Palauan'), (u'pli', u'Pali'), (u'pam', u'Pampanga; Kapampangan'), (u'pag', u'Pangasinan'), (u'pan', u'Panjabi; Punjabi'), (u'pap', u'Papiamento'), (u'paa', u'Papuan languages'), (u'nso', u'Pedi; Sepedi; Northern Sotho'), (u'fas', u'Persian'), (u'peo', u'Persian, Old (ca. 600-400 B.C.)'), (u'phi', u'Philippine languages'), (u'phn', u'Phoenician'), (u'pon', u'Pohnpeian'), (u'pol', u'Polish'), (u'por', u'Portuguese'), (u'pra', u'Prakrit languages'), (u'pro', u'Proven\xe7al, Old (to 1500); Occitan, Old (to 1500)'), (u'pus', u'Pushto; Pashto'), (u'que', u'Quechua'), (u'raj', u'Rajasthani'), (u'rap', u'Rapanui'), (u'rar', u'Rarotongan; Cook Islands Maori'), (u'qaa-qtz', u'Reserved for local use'), (u'roa', u'Romance languages'), (u'ron', u'Romanian'), (u'roh', u'Romansh'), (u'rom', u'Romany'), (u'run', u'Rundi'), (u'rus', u'Russian'), (u'sal', u'Salishan languages'), (u'sam', u'Samaritan Aramaic'), (u'smi', u'Sami languages'), (u'smo', u'Samoan'), (u'sad', u'Sandawe'), (u'sag', u'Sango'), (u'san', u'Sanskrit'), (u'sat', u'Santali'), (u'srd', u'Sardinian'), (u'sas', u'Sasak'), (u'sco', u'Scots'), (u'sel', u'Selkup'), (u'sem', u'Semitic languages'), (u'srp', u'Serbian'), (u'srr', u'Serer'), (u'shn', u'Shan'), (u'sna', u'Shona'), (u'iii', u'Sichuan Yi; Nuosu'), (u'scn', u'Sicilian'), (u'sid', u'Sidamo'), (u'sgn', u'Sign Languages'), (u'bla', u'Siksika'), (u'snd', u'Sindhi'), (u'sin', u'Sinhala; Sinhalese'), (u'sit', u'Sino-Tibetan languages'), (u'sio', u'Siouan languages'), (u'sms', u'Skolt Sami'), (u'den', u'Slave (Athapascan)'), (u'sla', u'Slavic languages'), (u'slk', u'Slovak'), (u'slv', u'Slovenian'), (u'sog', u'Sogdian'), (u'som', u'Somali'), (u'son', u'Songhai languages'), (u'snk', u'Soninke'), (u'wen', u'Sorbian languages'), (u'sot', u'Sotho, Southern'), (u'sai', u'South American Indian languages'), (u'alt', u'Southern Altai'), (u'sma', u'Southern Sami'), (u'spa', u'Spanish; Castilian'), (u'srn', u'Sranan Tongo'), (u'zgh', u'Standard Moroccan Tamazight'), (u'suk', u'Sukuma'), (u'sux', u'Sumerian'), (u'sun', u'Sundanese'), (u'sus', u'Susu'), (u'swa', u'Swahili'), (u'ssw', u'Swati'), (u'swe', u'Swedish'), (u'gsw', u'Swiss German; Alemannic; Alsatian'), (u'syr', u'Syriac'), (u'tgl', u'Tagalog'), (u'tah', u'Tahitian'), (u'tai', u'Tai languages'), (u'tgk', u'Tajik'), (u'tmh', u'Tamashek'), (u'tam', u'Tamil'), (u'tat', u'Tatar'), (u'tel', u'Telugu'), (u'ter', u'Tereno'), (u'tet', u'Tetum'), (u'tha', u'Thai'), (u'bod', u'Tibetan'), (u'tig', u'Tigre'), (u'tir', u'Tigrinya'), (u'tem', u'Timne'), (u'tiv', u'Tiv'), (u'tli', u'Tlingit'), (u'tpi', u'Tok Pisin'), (u'tkl', u'Tokelau'), (u'tog', u'Tonga (Nyasa)'), (u'ton', u'Tonga (Tonga Islands)'), (u'tsi', u'Tsimshian'), (u'tso', u'Tsonga'), (u'tsn', u'Tswana'), (u'tum', u'Tumbuka'), (u'tup', u'Tupi languages'), (u'tur', u'Turkish'), (u'ota', u'Turkish, Ottoman (1500-1928)'), (u'tuk', u'Turkmen'), (u'tvl', u'Tuvalu'), (u'tyv', u'Tuvinian'), (u'twi', u'Twi'), (u'udm', u'Udmurt'), (u'uga', u'Ugaritic'), (u'uig', u'Uighur; Uyghur'), (u'ukr', u'Ukrainian'), (u'umb', u'Umbundu'), (u'mis', u'Uncoded languages'), (u'und', u'Undetermined'), (u'hsb', u'Upper Sorbian'), (u'urd', u'Urdu'), (u'uzb', u'Uzbek'), (u'vai', u'Vai'), (u'ven', u'Venda'), (u'vie', u'Vietnamese'), (u'vol', u'Volap\xfck'), (u'vot', u'Votic'), (u'wak', u'Wakashan languages'), (u'wln', u'Walloon'), (u'war', u'Waray'), (u'was', u'Washo'), (u'cym', u'Welsh'), (u'fry', u'Western Frisian'), (u'wal', u'Wolaitta; Wolaytta'), (u'wol', u'Wolof'), (u'xho', u'Xhosa'), (u'sah', u'Yakut'), (u'yao', u'Yao'), (u'yap', u'Yapese'), (u'yid', u'Yiddish'), (u'yor', u'Yoruba'), (u'ypk', u'Yupik languages'), (u'znd', u'Zande languages'), (u'zap', u'Zapotec'), (u'zza', u'Zaza; Dimili; Dimli; Kirdki; Kirmanjki; Zazaki'), (u'zen', u'Zenaga'), (u'zha', u'Zhuang; Chuang'), (u'zul', u'Zulu'), (u'zun', u'Zuni'))

def profile_images_upload_path(instance, filename):
    try:
        filename = str(uuid.uuid4()) + '.' + str(filename.split('.')[1])
    except IndexError:
        filename = str(uuid.uuid4())

    path = "profile_images/"
    return os.path.join(path, filename)

def task_choices():
	choices = (
		('submission', 'Submission'),
		('review', 'Review'),
		('editing', 'Editing'),
		('production', 'Production'),
		('personal', 'Personal'),
	)
	return choices

def book_type_choices():
	return (
		('monograph', 'Monograph'),
		('edited_volume', 'Edited Volume'),
	)

class Profile(models.Model):
	user = models.OneToOneField(User)
	activation_code = models.CharField(max_length=100, null=True, blank=True)
	salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES, null=True, blank=True)
	middle_name = models.CharField(max_length=300, null=True, blank=True)
	biography = models.TextField(null=True, blank=True)
	orcid = models.CharField(max_length=40, null=True, blank=True, verbose_name="ORCiD")
	institution = models.CharField(max_length=1000)
	department = models.CharField(max_length=300, null=True, blank=True)
	country = models.CharField(max_length=300, choices=COUNTRY_CHOICES)
	twitter = models.CharField(max_length=300, null=True, blank=True, verbose_name="Twitter Handle")
	facebook = models.CharField(max_length=300, null=True, blank=True, verbose_name="Facebook Handle")
	linkedin = models.CharField(max_length=300, null=True, blank=True, verbose_name="Linkedin Profile")
	impactstory = models.CharField(max_length=300, null=True, blank=True, verbose_name="ImpactStory ID")
	github = models.CharField(max_length=300, null=True, blank=True, verbose_name="Github Username")
	profile_image = models.ImageField(upload_to=profile_images_upload_path, null=True, blank=True, storage=fs)
	email_sent = models.DateTimeField(blank=True, null=True)
	date_confirmed = models.DateTimeField(blank=True, null=True)
	confirmation_code = models.CharField(max_length=200, blank=True, null=True)
	roles = models.ManyToManyField('Role')

	def full_name(self):
		if self.middle_name:
			return "%s %s %s" % (self.user.first_name, self.middle_name, self.user.last_name)
		else:
			return "%s %s" % (self.user.first_name, self.user.last_name)

class Author(models.Model):
	first_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100)
	salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES, null=True, blank=True)
	institution = models.CharField(max_length=1000)
	department = models.CharField(max_length=300, null=True, blank=True)
	country = models.CharField(max_length=300, choices=COUNTRY_CHOICES)
	author_email = models.CharField(max_length=100)
	biography = models.TextField(max_length=3000, null=True, blank=True)
	orcid = models.CharField(max_length=40, null=True, blank=True, verbose_name="ORCiD")
	twitter = models.CharField(max_length=300, null=True, blank=True, verbose_name="Twitter Handle")
	linkedin = models.CharField(max_length=300, null=True, blank=True, verbose_name="Linkedin Profile")
	facebook = models.CharField(max_length=300, null=True, blank=True, verbose_name="Facebook Profile")
	sequence = models.IntegerField(default=1, null=True, blank=True)

	class Meta:
		ordering = ('sequence',)

	def __unicode__(self):
		return u'%s - %s %s' % (self.pk, self.first_name, self.last_name)

	def __repr__(self):
		return u'%s - %s %s' % (self.pk, self.first_name, self.last_name)

class Book(models.Model):
	prefix = models.CharField(max_length=100, null=True, blank=True)
	title = models.CharField(max_length=1000, null=True, blank=True)
	subtitle = models.CharField(max_length=1000, null=True, blank=True)
	series = models.ForeignKey('Series', null=True, blank=True, help_text="If you are submitting this work to an existing Series please selected it.")
	author = models.ManyToManyField('Author', null=True, blank=True)
	editor = models.ManyToManyField('Editor', null=True, blank=True)
	description = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Abstract")
	keywords = models.ManyToManyField('Keyword', null=True, blank=True)
	subject = models.ManyToManyField('Subject', null=True, blank=True)
	license = models.ForeignKey('License', null=True, blank=True, help_text="The license you recommend for this work.")
	cover = models.ImageField(null=True, blank=True)
	doi = models.CharField(max_length=25, null=True, blank=True)
	pages = models.CharField(max_length=10, null=True, blank=True)
	slug = models.CharField(max_length=1000, null=True, blank=True)
	cover_letter = models.TextField(null=True, blank=True, help_text="A covering letter for the Editors.")
	reviewer_suggestions = models.TextField(null=True, blank=True)
	competing_interests = models.TextField(null=True, blank=True, help_text="If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'")
	book_type = models.CharField(max_length=50, null=True, blank=True, choices=book_type_choices(), help_text="A monograph is a work authored, in its entirety, by one or more authors. An edited volume has different authors for each chapter.")

	# Book Owner
	owner = models.ForeignKey(User, null=True, blank=True)

	# Dates
	submission_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	publicaton_date = models.DateTimeField(null=True, blank=True)

	# Stage
	stage = models.ForeignKey('Stage', null=True, blank=True)
	submission_stage = models.IntegerField(null=True, blank=True)

	# Review
	review_assignments = models.ManyToManyField('ReviewAssignment', related_name='review', null=True, blank=True)
	review_form = models.ForeignKey('review.Form', null=True, blank=True)

	# Files
	files = models.ManyToManyField('File', null=True, blank=True)
	internal_review_files = models.ManyToManyField('File', null=True, blank=True, related_name='internal_review_files')
	external_review_files = models.ManyToManyField('File', null=True, blank=True, related_name='external_review_files')
	misc_files = models.ManyToManyField('File', null=True, blank=True, related_name='misc_files')

	# Contract
	contract = models.ForeignKey('Contract', null=True, blank=True)

	def __unicode__(self):
		return u'%s' % self.title

	def __repr__(self):
		return u'%s' % self.title

	def get_latest_review_round(self):
		try:
			return self.reviewround_set.all().order_by('-round_number')[0].round_number
		except IndexError:
			return 0

class Contract(models.Model):
	title = models.CharField(max_length=1000)
	notes = models.TextField(blank=True, null=True)
	editor_file = models.ForeignKey('File', related_name='editor_file', blank=True, null=True)
	author_file = models.ForeignKey('File', related_name='author_file', blank=True, null=True)
	editor_signed_off = models.DateField(blank=True, null=True)
	author_signed_off = models.DateField(blank=True, null=True)

	def __unicode__(self):
		return u'%s' % self.title

	def __repr__(self):
		return u'%s' % self.title

def review_type_choices():
	return (
		('internal', 'Internal'),
		('external', 'External'),
	)

def review_recommendation():
	return (
		('accept', 'Accept'),
		('reject', 'Reject'),
		('revisions', 'Revisions Required')
	)

class ReviewRound(models.Model):

	book = models.ForeignKey(Book)
	round_number = models.IntegerField()

	class Meta:
		unique_together = ('book', 'round_number')

	def __unicode__(self):
		return u'%s - %s round_number: %s' % (self.pk, self.book.title, self.round_number)

	def __repr__(self):
		return u'%s - %s round number: %s' %  (self.pk, self.book.title, self.round_number)

class ReviewAssignment(models.Model):
	book = models.ForeignKey(Book) #TODO: Remove this as it is already linked to the book through the review round
	review_round = models.ForeignKey(ReviewRound, blank=True, null=True)
	review_type = models.CharField(max_length=15, choices=review_type_choices())
	user = models.ForeignKey(User)
	assigned = models.DateField(auto_now=True)
	accepted = models.DateField(blank=True, null=True)
	declined = models.DateField(blank=True, null=True)
	due = models.DateField(blank=True, null=True)
	completed = models.DateField(blank=True, null=True)
	files = models.ManyToManyField('File', blank=True, null=True)
	body = models.TextField(blank=True, null=True)
	access_key = models.CharField(max_length=200)
	results = models.ForeignKey('review.FormResult', null=True, blank=True)
	recommendation = models.CharField(max_length=10, choices=review_recommendation(), null=True, blank=True)
	competing_interests = models.TextField(blank=True, null=True, help_text="If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'")

	class Meta:
		unique_together = ('book', 'user', 'review_type', 'review_round')

	def __unicode__(self):
		return u'%s - %s %s' % (self.pk, self.book.title, self.user.username)

	def __repr__(self):
		return u'%s - %s %s' %  (self.pk, self.book.title, self.user.username)



class License(models.Model):
	name = models.CharField(max_length=1000)
	short_name = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	version = models.CharField(max_length=10)
	url = models.URLField(null=True, blank=True)

	def __unicode__(self):
		return u'%s' % self.short_name

	def __repr__(self):
		return u'%s' % self.short_name

class Series(models.Model):
	name = models.CharField(max_length=100)
	editor = models.ForeignKey(User, null=True, blank=True)
	issn = models.CharField(max_length=15)
	description = models.TextField(null=True, blank=True)
	url = models.URLField(null=True, blank=True)

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

class Editor(models.Model):
	first_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100)
	salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES, null=True, blank=True)
	institution = models.CharField(max_length=1000)
	department = models.CharField(max_length=300, null=True, blank=True)
	country = models.CharField(max_length=300, choices=COUNTRY_CHOICES)
	author_email = models.CharField(max_length=100)
	biography = models.TextField(max_length=3000, null=True, blank=True)
	orcid = models.CharField(max_length=40, null=True, blank=True, verbose_name="ORCiD")
	twitter = models.CharField(max_length=300, null=True, blank=True, verbose_name="Twitter Handle")
	linkedin = models.CharField(max_length=300, null=True, blank=True, verbose_name="Linkedin Profile")
	facebook = models.CharField(max_length=300, null=True, blank=True, verbose_name="Facebook Profile")
	sequence = models.IntegerField(default=1, null=True, blank=True)

	class Meta:
		ordering = ('sequence',)

	def __unicode__(self):
		return u'%s - %s %s' % (self.pk, self.first_name, self.last_name)

	def __repr__(self):
		return u'%s - %s %s' % (self.pk, self.first_name, self.last_name)

class File(models.Model):
	mime_type = models.CharField(max_length=50)
	original_filename = models.CharField(max_length=1000)
	uuid_filename = models.CharField(max_length=100)
	label = models.CharField(max_length=200, null=True, blank=True)
	description = models.CharField(max_length=1000, null=True, blank=True)
	date_uploaded = models.DateTimeField(auto_now=True)
	stage_uploaded = models.IntegerField()
	kind = models.CharField(max_length=100)
	sequence = models.IntegerField(default=1)

	def __unicode__(self):
		return u'%s' % self.original_filename

	def __repr__(self):
		return u'%s' % self.original_filename

	class Meta:
		ordering = ('sequence', '-kind')

class FileVersion(models.Model):
	file = models.ForeignKey(File)
	original_filename = models.CharField(max_length=1000)
	uuid_filename = models.CharField(max_length=100)
	date_uploaded = models.DateTimeField()

	class Meta:
		ordering = ('-date_uploaded',)

class Subject(models.Model):
	name = models.CharField(max_length=250)

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

class Keyword(models.Model):
	name = models.CharField(max_length=250)

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

stage_choices = (
	('proposal', 'Proposal'),
	('submission', 'New Submission'),
	('review', 'Review'),
	('editing', 'Editing'),
	('production', 'Production'),
	('published', 'Published'),
	('declined', 'Declined'),
)

class Stage(models.Model):
	current_stage = models.CharField(max_length="20", choices=stage_choices, null=True, blank=True)
	proposal = models.DateTimeField(null=True, blank=True)
	submission = models.DateTimeField(null=True, blank=True)
	review = models.DateTimeField(null=True, blank=True)
	internal_review = models.DateTimeField(null=True, blank=True)
	external_review = models.DateTimeField(null=True, blank=True)
	editing = models.DateTimeField(null=True, blank=True)
	production = models.DateTimeField(null=True, blank=True)
	publication = models.DateTimeField(null=True, blank=True)
	declined = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return u'%s' % self.current_stage

	def __repr__(self):
		return u'%s' % self.current_stage

class Task(models.Model):
	book = models.ForeignKey(Book, null=True, blank=True)
	creator = models.ForeignKey(User, related_name='creator')
	assignee = models.ForeignKey(User, related_name='assignee')
	text = models.CharField(max_length=200)
	workflow = models.CharField(max_length=50, choices=task_choices())
	assigned = models.DateField(auto_now_add=True, null=True, blank=True)
	due = models.DateField(null=True, blank=True)
	completed = models.DateField(null=True, blank=True)

class Role(models.Model):
	name = models.CharField(max_length=100)
	slug = models.CharField(max_length=100)

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

log_choices = (
	('submission', 'Submission'),
	('workflow', 'Workflow'),
	('file', 'File'),
)

class Log(models.Model):
	book = models.ForeignKey(Book)
	user = models.ForeignKey(User)
	kind = models.CharField(max_length=100, choices=log_choices)
	short_name = models.CharField(max_length=100)
	message = models.TextField()
	date_logged = models.DateTimeField(auto_now_add=True, null=True, blank=True)

setting_types = (
	('rich_text', 'Rich Text'),
	('text', 'Text'),
	('char', 'Characters'),
	('number', 'Number'),
	('boolean', 'Boolean'),
	('file', 'File'),
)

class SettingGroup(models.Model):
	name = models.CharField(max_length=100)
	enabled = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

class Setting(models.Model):
	name = models.CharField(max_length=100)
	group = models.ForeignKey(SettingGroup)
	types = models.CharField(max_length=20, choices=setting_types)
	value = models.TextField(null=True, blank=True)

	class Meta:
		ordering = ('group', 'name')

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

class Format(models.Model):
	book = models.ForeignKey(Book)
	file = models.ForeignKey(File)
	name = models.CharField(max_length=200)
	indentifier = models.CharField(max_length=200, unique=True)
	sequence = models.IntegerField(default=9999)

	class Meta:
		ordering = ('sequence', 'name')

	def __unicode__(self):
		return u'%s - %s' % (self.book, self.indentifier)

	def __repr__(self):
		return u'%s - %s' % (self.book, self.indentifier)

class Chapter(models.Model):
	book = models.ForeignKey(Book)
	file = models.ForeignKey(File)
	name = models.CharField(max_length=200)
	indentifier = models.CharField(max_length=200, unique=True)
	sequence = models.IntegerField(default=9999)

	class Meta:
		ordering = ('sequence', 'name')

	def __unicode__(self):
		return u'%s - %s' % (self.book, self.indentifier)

	def __repr__(self):
		return u'%s - %s' % (self.book, self.indentifier)
