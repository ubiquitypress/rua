from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns('',
	url(r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/access_key/(?P<access_key>[-\w+]+)/$', 'review.views.review', name='review_with_access_key'),
)
