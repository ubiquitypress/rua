from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns('',
	
	url(r'dashboard/$', 'review.views.reviewer_dashboard', name='reviewer_dashboard'),

	# Reviewer decision
	url(r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/(?P<review_assignment>\d+)/decision/$', 'review.views.reviewer_decision', name='reviewer_decision_without'),
	url(r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/(?P<review_assignment>\d+)/decision/(?P<decision>[-\w]+)/$', 'review.views.reviewer_decision', name='reviewer_decision_with'),
	url(r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/(?P<review_assignment>\d+)/access_key/(?P<access_key>[-\w+]+)/decision/$', 'review.views.reviewer_decision', name='reviewer_decision_without_access_key'),
	url(r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/(?P<review_assignment>\d+)/access_key/(?P<access_key>[-\w+]+)/decision/(?P<decision>[-\w]+)/$', 'review.views.reviewer_decision', name='reviewer_decision_with_access_key'),

	
	# Review	
	url(r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/(?P<review_round>\d+)/access_key/(?P<access_key>[-\w+]+)/$', 'review.views.review', name='review_with_access_key'),
	url(r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/(?P<review_round>\d+)/$', 'review.views.review', name='review_without_access_key'),
	url(r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/(?P<review_round>\d+)/complete/$', 'review.views.review_complete', name='review_complete'),
	url(r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/(?P<review_round>\d+)/access_key/(?P<access_key>[-\w+]+)/complete/$', 'review.views.review_complete', name='review_complete_with_access_key'),
	url(r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/(?P<review_round>\d+)/complete/no-redirect/$', 'review.views.review_complete_no_redirect', name='review_complete_no_redirect'),
	url(r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/(?P<review_round>\d+)/access_key/(?P<access_key>[-\w+]+)/complete/no-redirect/$', 'review.views.review_complete_no_redirect', name='review_complete_with_access_key_no_redirect'),

)
