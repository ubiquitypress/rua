from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Review
	    url(r'$', 'onetasker.views.dashboard', name='onetasker_dashboard'),
	    #url(r'^submission/(?P<submission_id>\d+)/$', 'author.views.author_submission', name='author_submission'),
)
