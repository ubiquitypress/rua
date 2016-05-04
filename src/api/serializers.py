from django.contrib.auth.models import User

from core import models
from review import models as review_models
from rest_framework import serializers
import json
from django.core import serializers as serializers_alt
from pprint import pprint

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Author
        fields = (
        'id',
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
        'id',
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

class ReviewRoundSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.ReviewRound
        fields = (
            'round_number',
            'date_started',
        )

class FormResultSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = review_models.FormResult
        fields = (
            'data',
            'date',
        )

class ReviewAssignmentSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer()
    review_round = ReviewRoundSerializer()
    results = FormResultSerializer()

    class Meta:
        model = models.ReviewAssignment
        fields = (
            'review_round',
            'review_type',
            'user',
            'assigned',
            'accepted',
            'declined',
            'due',
            'completed',
            'competing_interests',
            'recommendation',
            'results',
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
            'id',
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
            'id',
            'file',
            'name',
            'identifier',
            'file_type',
            'sequence',
        )


class ChapterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Chapter
        fields = (
            'id',
            'formats',
            'blurbs',
            'keywords',
            'disciplines',
            'sequence',
        )


class PhysicalFormatSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Format
        fields = (
            'id',
            'name',
            'file_type',
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
            'id',
            'identifier',
            'value',
            'displayed',
            'object_type',
            'object_id',
        )

class LanguageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Language
        fields = (
            'code',
            'display',
        )

class LicenseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.License
        fields = (
            'name',
            'short_name',
            'version',
            'url',
            'description',
        )

class BookSerializer(serializers.HyperlinkedModelSerializer):
    license = serializers.ReadOnlyField(source='license.short_name')
    author = AuthorSerializer(many=True)
    editor = EditorSerializer(many=True)
    keywords = KeywordSerializer(many=True)
    subject = SubjectSerializer(many=True)
    identifier = IdentiferSerializer(many=True, source='identifier_set', required=False)

    class Meta:
        model = models.Book
        fields = (
            'id',
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
            'identifier',
            'peer_review_override',
            )

class JuraBookSerializer(serializers.HyperlinkedModelSerializer):
    """
    This serializer is used only by Ubiquity press
    """
    license = serializers.ReadOnlyField(source='license.code')
    author = AuthorSerializer(many=True)
    editor = EditorSerializer(many=True)
    keywords = KeywordSerializer(many=True)
    subject = SubjectSerializer(many=True)
    formats = FormatSerializer(many=True)
    chapters = serializers.SerializerMethodField('chapters_retrieve')
    physical_formats = PhysicalFormatSerializer(many=True,  source='physicalformat_set')
    stage = StageSerializer(many=False)
    identifier = IdentiferSerializer(many=True, source='identifier_set', required=False)
    languages = LanguageSerializer(many=True)
    review_assignments = ReviewAssignmentSerializer(many=True)

    class Meta:
        model = models.Book
        fields = (
            'id',
            'slug',
            'prefix',
            'title',
            'subtitle',
            'cover',
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
            'languages',
            'review_type',
            'formats',
            'chapters',
            'physical_formats',
            'stage',
            'identifier',
            'peer_review_override',
            'review_assignments',
            )
    def chapters_retrieve(self, book):
        chapter_list = []
        chapters =  models.Chapter.objects.filter(book=book)
        for chapter in chapters:
            chapter_dict = {}

            keywords_list = []
            for keyword in chapter.keywords.all():
                keywords_list.append(keyword.name)

            disciplines_list = []
            for discipline in chapter.disciplines.all():
                disciplines_list.append(discipline.name)

            chapter_dict['keywords'] = keywords_list
            chapter_dict['disciplines'] = disciplines_list
            chapter_dict['sequence'] = chapter.sequence
            chapter_dict['blurbs'] = chapter.blurbs
            formats = chapter.formats.all()
            format_list = []
            for chapter_format in formats:
                chapter_format_dict = {}
                chapter_format_dict['name'] = chapter_format.name
                chapter_format_dict['sequence'] = chapter_format.sequence
                chapter_format_dict['file_type'] = chapter_format.file_type
                chapter_format_dict['identifier'] = chapter_format.identifier
                chapter_format_dict['file_pk'] = chapter_format.file.pk
                format_list.append(chapter_format_dict)
            chapter_dict['formats'] = format_list
            chapter_list.append(chapter_dict)

        return chapter_list

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        keyword_data = validated_data.pop('keywords')
        lang_data = validated_data.pop('languages')
        subject_data = validated_data.pop('subject')
        stage_data = validated_data.pop('stage')

        pprint(validated_data)

        book = models.Book.objects.create(**validated_data)

        stage = models.Stage.objects.create(book=book, current_stage="published")

        for author in author_data:
            author = models.Author.objects.create(book=book, **author_data)



        return book

class OMPSerializer(serializers.HyperlinkedModelSerializer):
    """
    This serializer is used only by Ubiquity press
    """
    license = serializers.ReadOnlyField(source='license.code')
    author = AuthorSerializer(many=True)
    keywords = KeywordSerializer(many=True)
    subject = SubjectSerializer(many=True)
    stage = StageSerializer(many=False)
    identifier = IdentiferSerializer(many=True, source='identifier_set', required=False)
    languages = LanguageSerializer(many=True)

    class Meta:
        model = models.Book
        fields = (
            'id',
            'slug',
            'prefix',
            'title',
            'subtitle',
            'cover',
            'submission_date',
            'publication_date',
            #'series',
            'license',
            'pages',
            'book_type',
            'author',
            'description',
            'keywords',
            'subject',
            'languages',
            'review_type',
            'stage',
            'identifier',
            )

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        keyword_data = validated_data.pop('keywords')
        lang_data = validated_data.pop('languages')
        subject_data = validated_data.pop('subject')
        stage_data = validated_data.pop('stage')

        pprint(validated_data)
        book = models.Book.objects.create(**validated_data)
        stage = models.Stage.objects.create(current_stage="published")
        book.stage = stage

        for author in author_data:
            author = models.Author.objects.create(**author)
            book.author.add(author)

        for language in lang_data:
            lang, c = models.Language.objects.get_or_create(**language)
            book.languages.add(lang)

        for subject in subject_data:
            subj, c = models.Subject.objects.get_or_create(**subject)
            book.subject.add(subj)

        for keyword in keyword_data:
            keyw, c = models.Keyword.objects.get_or_create(**keyword)
            book.keywords.add(keyw)


        book.save()
        return book


