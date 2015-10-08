from core import models
from rest_framework import serializers

class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Author
        fields = (
        'salutation',
        'first_name',
        'middle_name',
        'last_name',
        'institution',
        'department',
        'country',
        'author_email',
        'biography',
        'orcid',
        'twitter',
        'linkedin',
        'facebook',
        'sequence',
        )

class EditorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Editor
        fields = (
        'salutation',
        'first_name',
        'middle_name',
        'last_name',
        'institution',
        'department',
        'country',
        'author_email',
        'biography',
        'orcid',
        'twitter',
        'linkedin',
        'facebook',
        'sequence',
        )

class KeywordSerializer(serializers.HyperlinkedModelSerializer):

     class Meta:
         model = models.Keyword
         fields = ('name',)

class SubjectSerializer(serializers.HyperlinkedModelSerializer):

     class Meta:
         model = models.Subject
         fields = ('name',)

class FileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.File
        fields = (
            'label',
            'original_filename',
            'uuid_filename',
            'mime_type',
            'kind',
            'sequence',
        )

class FormatSerializer(serializers.HyperlinkedModelSerializer):

    file = FileSerializer(many=False)

    class Meta:
        model = models.Format
        fields = (
            'file',
            'name',
            'identifier',
            'sequence',
        )

class StageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Stage
        fields = (
            'current_stage',
            'proposal',
            'submission',
            'review',
            'internal_review',
            'external_review',
            'editing',
            'production',
            'publication',
            'declined',
        )

class IdentiferSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Identifier
        fields = (
            'identifier',
            'value',
            'displayed',
        )

class BookSerializer(serializers.HyperlinkedModelSerializer):
    license = serializers.ReadOnlyField(source='license.short_name')
    author = AuthorSerializer(many=True)
    editor = EditorSerializer(many=True)
    keywords = KeywordSerializer(many=True)
    subject = SubjectSerializer(many=True)
    identifier = IdentiferSerializer(many=True, source='identifier_set')

    class Meta:
        model = models.Book
        fields = (
            'slug',
            'prefix',
            'title',
            'subtitle',
            'submission_date',
            'publication_date',
            #'series',
            'license',
            'pages',
            'book_type',
            'author',
            'editor',
            'description',
            'keywords',
            'subject',
            'review_type',
            'identifier'
            )

class JuraBookSerializer(serializers.HyperlinkedModelSerializer):
    """
    This serializer is used only by Ubiquity press
    """
    license = serializers.ReadOnlyField(source='license.short_name')
    author = AuthorSerializer(many=True)
    editor = EditorSerializer(many=True)
    keywords = KeywordSerializer(many=True)
    subject = SubjectSerializer(many=True)
    formats = FormatSerializer(many=True)
    stage = StageSerializer(many=False)
    identifier = IdentiferSerializer(many=True, source='identifier_set')

    class Meta:
        model = models.Book
        fields = (
            'slug',
            'prefix',
            'title',
            'subtitle',
            'submission_date',
            'publication_date',
            #'series',
            'license',
            'pages',
            'book_type',
            'author',
            'editor',
            'description',
            'keywords',
            'subject',
            'review_type',
            'formats',
            'stage',
            'identifier',
            )
