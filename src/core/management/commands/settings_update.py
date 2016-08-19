import os
import json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core import models


class Command(BaseCommand):
    help = "Run 'python manage.py settings_update <setting_name>' to update or create the specified setting."

    def add_arguments(self, parser):
        parser.add_argument('setting_name')

    def handle(self, *args, **options):
        file = os.path.join(settings.BASE_DIR, 'core/fixtures/settinggroups.json')

        with open(file) as json_data:
            default_data = json.load(json_data)
            setting = default_data.get('name' == args[0])

            try:
                group = models.SettingGroup.objects.get(pk=int(setting['fields'].get('group')))

                defaults = {
                    'group': group,
                    'types': setting['fields'].get('types'),
                    'value': setting['fields'].get('value'),
                    'description': setting['fields'].get('description'),
                },

                s, created = models.Setting.objects.update_or_create(
                    name=setting['fields'].get('name'),
                    defaults=defaults
                )

                if created:
                    print 'Created setting {0}'.format(s.name)

            except setting.DoesNotExist:
                raise CommandError('Setting {0} not found'.format(setting))
