from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # Core Site
    url(r'^admin/', include(admin.site.urls)),
    url(r'^submission/', include('submission.urls')),
    url(r'^workflow/', include('workflow.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^review/', include('review.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^author/', include('author.urls')),
    url(r'^editor/', include('editor.urls')),
    url(r'^tasks/', include('onetasker.urls')),

    # 3rd Party Apps
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Public pages
    url(r'^$', 'core.views.index', name='index'),
    url(r'^contact/$', 'core.views.contact', name='contact'),

    # Login/Register
    url(r'^login/$', 'core.views.login', name='login'),
    url(r'^logout/$', 'core.views.logout', name='logout'),
    url(r'^register/$', 'core.views.register', name='register'),
    url(r'^login/activate/(?P<code>[-\w./]+)/$', 'core.views.activate', name='activate'),

    # Unauthenticated password reset
    url(r'^login/reset/$', 'core.views.unauth_reset', name='unauth_reset'),

    # User profile
    url(r'^user/$', 'core.views.user_home', name='user_home'),
    url(r'^user/profile/$', 'core.views.view_profile', name='view_profile'),
    url(r'^user/profile/update/$', 'core.views.update_profile', name='update_profile'),
    url(r'^user/profile/resetpassword/$', 'core.views.reset_password', name='reset_password'),
    url(r'^user/task/new/$', 'core.views.task_new', name='task_new'),
    url(r'^user/task/(?P<task_id>[-\w./]+)/complete/$', 'core.views.task_complete', name='task_complete'),

    # Message AJAX
    url(r'^book/(?P<book_id>\d+)/message/new/$', 'core.views.new_message', name='new_message'),

    # User submission
    url(r'^user/submission/(?P<submission_id>\d+)/$', 'core.views.user_submission', name='user_submission'),
    
    url(r'overview/$', 'core.views.overview', name='overview'),

    # Email
    url(r'^email/authors/submission/(?P<submission_id>\d+)/$', 'core.views.email_authors', name='email_authors'),
    url(r'^email/authors/submission/(?P<submission_id>\d+)/author/(?P<author_id>\d+)/$', 'core.views.email_authors', name='email_author'),
    url(r'^email/get/authors/$', 'core.views.get_authors', name='get_authors'),
    # Files
    url(r'^files/user/submission/(?P<submission_id>\d+)/file/(?P<file_id>\d+)/download/$', 'core.views.serve_file', name='serve_file'),
    url(r'^files/submission/(?P<submission_id>\d+)/file/(?P<revision_id>\d+)/download_versioned_file/$', 'core.views.serve_versioned_file', name='serve_versioned_file'),
    url(r'^files/submission/(?P<submission_id>\d+)/file/(?P<file_id>\d+)/delete/returner/(?P<returner>[-\w]+)/$', 'core.views.delete_file', name='delete_file'),
    url(r'^files/submission/(?P<submission_id>\d+)/file/(?P<file_id>\d+)/view/$', 'core.views.view_file', name='view_file'),
    url(r'^files/submission/(?P<submission_id>\d+)/file/(?P<file_id>\d+)/update/returner/(?P<returner>[-\w]+)/$', 'core.views.update_file', name='update_file'),
    url(r'^files/submission/(?P<submission_id>\d+)/file/(?P<file_id>\d+)/versions/$', 'core.views.versions_file', name='versions_file'),

    #log
    url(r'^log/submission/(?P<submission_id>\d+)/', 'core.views.view_log', name='view_log'),

    url(r'^misc_files/(?P<submission_id>\d+)/upload/$', 'core.views.upload_misc_file', name='upload_misc_file'),
)

handler403 = 'core.views.permission_denied'

# Allow Django to serve static content only in debug/dev mode
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^404/$', TemplateView.as_view(template_name='core/404.html')),
        url(r'^500/$', TemplateView.as_view(template_name='core/500.html')),
    )
