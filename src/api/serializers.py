from core import models
from rest_framework import serializers

class BookSerializer(serializers.HyperlinkedModelSerializer):
    license = serializers.ReadOnlyField(source='license.short_name')
    class Meta:
        model = models.Book
        fields = (
            'slug',
            'prefix',
            'title',
            'subtitle',
            'book_type',
            'series',
            'license',
            'authors_or_editors',
            'description'
        )
