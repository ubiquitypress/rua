from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns('',
	# Review
	url(r'^book/(?P<submission_id>\d+)/edit/(?P<copyedit_id>\d+)/$', 'copyedit.views.copyedit', name='copyedit'),
	url(r'^book/(?P<submission_id>\d+)/edit/(?P<copyedit_id>\d+)/files/$', 'copyedit.views.copyedit_files', name='copyedit_files'),
	url(r'^book/(?P<submission_id>\d+)/edit/(?P<copyedit_id>\d+)/complete/$', 'copyedit.views.copyedit_complete', name='copyedit_complete'),

	url(r'^book/(?P<submission_id>\d+)/edit/(?P<copyedit_id>\d+)/author/$', 'copyedit.views.copyedit_author', name='copyedit_author'),
)
