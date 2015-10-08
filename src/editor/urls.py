from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Review
	    url(r'dashboard/$', 'editor.views.editor_dashboard', name='editor_dashboard'),
	    url(r'^submission/(?P<submission_id>\d+)/$', 'editor.views.editor_submission', name='editor_submission'),
	    url(r'^submission/(?P<submission_id>\d+)/tasks/$', 'editor.views.editor_tasks', name='editor_tasks'),
	    url(r'^submission/(?P<submission_id>\d+)/status/$', 'editor.views.editor_status', name='editor_status'),

	    url(r'^submission/(?P<submission_id>\d+)/review/$', 'editor.views.editor_review', name='editor_review'),
	    url(r'^submission/(?P<submission_id>\d+)/review/round/(?P<round_number>\d+)/$', 'editor.views.editor_review_round', name='editor_review_round'),
	    url(r'^submission/(?P<submission_id>\d+)/files/(?P<review_type>[-\w]+)/add/$', 'editor.views.add_review_files', name='add_review_files'),
	    url(r'^submission/(?P<submission_id>\d+)/files/(?P<file_id>\d+)/(?P<review_type>[-\w]+)/delete/$', 'editor.views.delete_review_files', name='delete_review_files'),
	)
