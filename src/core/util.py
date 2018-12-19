from bs4 import BeautifulSoup

from core import models


def get_setting(setting_name, setting_group_name, default=None):
    try:
        setting = models.Setting.objects.get(
            name=setting_name,
            group__name=setting_group_name,
        )
        return setting.value
    except models.Setting.DoesNotExist:
        if default:
            return default
        return ''


def strip_html_tags(raw_html):
    return BeautifulSoup(raw_html, "html.parser").get_text()