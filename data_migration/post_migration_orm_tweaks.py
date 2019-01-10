"""This script is intended to copied and pasted into a Django shell.
In the interests of cleanliness, this code should be idempotent.
Running it more than once should have the same effect as running it once.
"""

# Amend the paths of book covers
from core.models import Book
books = Book.objects.all()
for book in books:
    if book.cover and 'files/media' not in book.cover.name:
        book.cover = f'files/media/{book.cover.name}'
        book.save()


# Fix brand-header and favicon settings
from core.models import Setting

brand_header_setting = Setting.objects.get(name='brand_header')
if (
        brand_header_setting.value and
        'files/media/settings' not in brand_header_setting.value
):
    brand_header_setting.value = (
        f'files/media/settings/{brand_header_setting.value}'
    )
    brand_header_setting.save()

favicon_setting = Setting.objects.get(name='favicon')
if (
        favicon_setting.value and
        'files/media/settings' not in favicon_setting.value
):
    favicon_setting.value = (
        f'files/media/settings/{brand_header_setting.value}'
    )
    favicon_setting.save()
