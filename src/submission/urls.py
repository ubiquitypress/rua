from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

	 url(r'^$', 'submission.views.start_submission', name='submission_start'),
)