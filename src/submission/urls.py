from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

	url(r'^book/new/stage/one/$', 'submission.views.start_submission', name='submission_start'),
	url(r'^book/(?P<book_id>\d+)/stage/one/$', 'submission.views.start_submission', name='edit_start'),
	url(r'^book/(?P<book_id>\d+)/stage/two/$', 'submission.views.submission_two', name='submission_two'),
	url(r'^book/(?P<book_id>\d+)/stage/three/$', 'submission.views.submission_three', name='submission_three'),
	url(r'^book/(?P<book_id>\d+)/stage/four/$', 'submission.views.submission_four', name='submission_four'),
	url(r'^book/(?P<book_id>\d+)/stage/four/author/new/$', 'submission.views.author', name='author'),
	url(r'^book/(?P<book_id>\d+)/stage/four/author/(?P<author_id>\d+)/$', 'submission.views.author', name='author_edit'),
	url(r'^book/(?P<book_id>\d+)/stage/four/editor/new/$', 'submission.views.editor', name='editor'),
	url(r'^book/(?P<book_id>\d+)/stage/four/editor/(?P<editor_id>\d+)/$', 'submission.views.editor', name='editor_edit'),
	url(r'^book/(?P<book_id>\d+)/stage/five/$', 'submission.views.submission_five', name='submission_five'),

	# Ajax url
	url(r'^book/(?P<book_id>\d+)/order/(?P<type_to_handle>[-\w./]+)/$', 'submission.views.file_order', name='file_order'),

	url(r'^proposal/$', 'submission.views.start_proposal', name='proposal_start'),
)
