from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Review
	    url(r'dashboard/$', 'author.views.author_dashboard', name='author_dashboard'),
	    url(r'^submission/(?P<submission_id>\d+)/$', 'author.views.author_submission', name='author_submission'),
)
