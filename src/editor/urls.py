from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Review
	    url(r'dashboard/$', 'editor.views.editor_dashboard', name='editor_dashboard'),
	    url(r'^submission/(?P<submission_id>\d+)/$', 'editor.views.editor_submission', name='editor_submission'),
	    url(r'^submission/(?P<submission_id>\d+)/review/$', 'editor.views.editor_review', name='editor_review'),
	)
