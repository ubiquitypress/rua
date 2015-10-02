from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Review
	    url(r'dashboard/$', 'author.views.author_dashboard', name='author_dashboard'),
	    url(r'^submission/(?P<submission_id>\d+)/$', 'author.views.author_submission', name='author_submission'),
	    url(r'^submission/(?P<submission_id>\d+)/status/$', 'author.views.status', name='status'),
	    url(r'^submission/(?P<submission_id>\d+)/contract/(?P<contract_id>\d+)/signoff/$', 'author.views.author_contract_signoff', name='author_contract_signoff'),
)
