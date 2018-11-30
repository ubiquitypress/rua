from base_settings import *

DEBUG = True

SECRET_KEY = '_%@8*2$*1*i&um4+#a6w(%xqa_19=tfmhu9u-l*7t(a$g(2)wg'


ALLOWED_HOSTS = [
    host.strip() for host in
    os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')
]


# ## DATABASE ##

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.getenv('DATABASE_NAME', 'rua'),
        'USER': os.getenv('DATABASE_USER', 'root'),
        'PASSWORD': os.getenv('DATABASE_PASS', ''),
        'HOST': os.getenv('DATABASE_HOST', '127.0.0.1'),
        'PORT': os.getenv('DATABASE_PORT', '3306')
    }
}

# ## LOGGING ##

LOGGING = None
SENTRY_RELEASE = None
RAVEN_CONFIG = None
