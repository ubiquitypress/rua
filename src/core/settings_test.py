from .settings_dev import *


SECRET_KEY = '_%@8*2$*1*i&um4+#a6w(%xqa_19=tfmhu9u-l*7t(a$g(2)wg'


# ## DATABASE ##

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': os.getenv('DATABASE_NAME', 'postgres'),
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DATABASE_PASS', 'postgres'),
        'HOST': os.getenv('DATABASE_HOST', 'db'),
        'PORT': os.getenv('DATABASE_PORT', '5432')
    }
}

DEBUG = False
DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
STATICFILES_STORAGE = 'inmemorystorage.InMemoryStorage'
LOGGING = {}
