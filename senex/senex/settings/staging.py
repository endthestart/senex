from os.path import join, normpath
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "senex_staging",
        "USER": "senex",
        "PASSWORD": "h3xag0n",
        "HOST": "localhost",
        "PORT": "",
    }
}

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION

########## STATIC FILES CONFIGURATION
STATIC_ROOT = normpath(join(SITE_ROOT, '../static'))
########## END OF STATIC FILES CONFIGURATION
