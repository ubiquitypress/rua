from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Review
	url(r'^book/(?P<submission_id>\d+)/typeset/(?P<typeset_id>\d+)/$', 'typeset.views.typeset', name='typeset'),
	url(r'^book/(?P<submission_id>\d+)/typeset/(?P<typeset_id>\d+)/files/$', 'typeset.views.typeset_files', name='typeset_files'),
	url(r'^book/(?P<submission_id>\d+)/typeset/(?P<typeset_id>\d+)/complete/$', 'typeset.views.typeset_complete', name='typeset_complete'),
	url(r'^book/(?P<submission_id>\d+)/typeset/(?P<typeset_id>\d+)/author/$', 'typeset.views.typeset_author', name='typeset_author'),
)
