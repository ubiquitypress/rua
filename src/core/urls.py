from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # Core Site
    url(r'^admin/', include(admin.site.urls)),
    url(r'^submission/', include('submission.urls')),
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
)

# Allow Django to serve static content only in debug/dev mode
if settings.DEBUG:
    urlpatterns += patterns('', 
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),
        url(r'^500/$', TemplateView.as_view(template_name='500.html')),
    )