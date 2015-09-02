from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Review
	url(r'^book/(?P<submission_id>\d+)/index/(?P<index_id>\d+)/$', 'indexing.views.index', name='index'),
	url(r'^book/(?P<submission_id>\d+)/index/(?P<index_id>\d+)/files/$', 'indexing.views.index_files', name='index_files'),
	url(r'^book/(?P<submission_id>\d+)/index/(?P<index_id>\d+)/complete/$', 'indexing.views.index_complete', name='index_complete'),
)
