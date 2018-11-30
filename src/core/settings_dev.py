from base_settings import *


SECRET_KEY = '_%@8*2$*1*i&um4+#a6w(%xqa_19=tfmhu9u-l*7t(a$g(2)wg'

ALLOWED_HOSTS = [
    host.strip() for host in
    os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')
]



DEBUG = True

# ## LOGGING ##

LOGGING = None
SENTRY_RELEASE = None
RAVEN_CONFIG = None
