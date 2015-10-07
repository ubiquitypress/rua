from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Review
	    url(r'^$', 'onetasker.views.dashboard', name='onetasker_dashboard'),
	    url(r'^(?P<assignment_type>[-\w]+)/(?P<assignment_id>\d+)$', 'onetasker.views.task_hub', name='onetasker_task_hub'),
	    url(r'^(?P<assignment_type>[-\w]+)/(?P<assignment_id>\d+)/(?P<about>[-\w]+)$', 'onetasker.views.task_hub', name='onetasker_task_about'),
	    #url(r'^submission/(?P<submission_id>\d+)/$', 'author.views.author_submission', name='author_submission'),
)
