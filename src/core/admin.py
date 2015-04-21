from django.contrib import admin
from models import *

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_email','first_name', 'last_name', 'orcid', 'institution')
    search_fields = ('author_email', 'first_name', 'last_name')

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'institution', 'date_confirmed')
	search_fields = ('orcid', 'institution', 'biography', )

class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'license')
	search_fields = ('title', 'doi', 'publication_date')

class LicenseAdmin(admin.ModelAdmin):
	list_display = ('name', 'short_name')
	search_fields = ('name', 'short_name')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('assignee', 'creator', 'text', 'workflow')
    list_filter = ('workflow', 'assignee')
    search_fields = ('text',)

admin_list = [
    (Author, AuthorAdmin),
    (Profile, ProfileAdmin),
    (Book, BookAdmin),
    (License, LicenseAdmin),
    (Task, TaskAdmin),
    (Files,),
    (Stage,),
    (Subject,),
    (Keyword,),
    (Series,),
]

[admin.site.register(*t) for t in admin_list]