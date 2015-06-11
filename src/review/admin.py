from django.contrib import admin
from models import *

# Register your models here.
class FormElementInline(admin.TabularInline):
    model = Form.fields.through

class FormAdmin(admin.ModelAdmin):
	list_display = ('name', 'ref')
	search_fields = ('name',)
	exclude = ("fields", )
	inlines = (FormElementInline,)

class FormElementAdmin(admin.ModelAdmin):
	list_display = ('name', 'field_type')

class FormResultAdmin(admin.ModelAdmin):
	list_display = ('form', 'date')

admin_list = [
    (Form, FormAdmin),
    (FormElement, FormElementAdmin),
    (FormResult, FormResultAdmin),
]

[admin.site.register(*t) for t in admin_list]
