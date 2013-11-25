from os.path import join, normpath
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

########## MEDIA FILES CONFIGURATION
MEDIA_ROOT = normpath(join(SITE_ROOT, '../media'))
MEDIA_URL = '/media/'
########## END OF MEDIA FILES CONFIGURATION

########## STATIC FILES CONFIGURATION
STATIC_ROOT = normpath(join(SITE_ROOT, '../static'))
STATIC_URL = '/static/'
########## END OF STATIC FILES CONFIGURATION

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "senex.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
        }
}

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
########## END CACHE CONFIGURATION

########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}
