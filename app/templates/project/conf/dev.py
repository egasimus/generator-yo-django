from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )

DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql',
                         'NAME': '<%= dbName %>',
                         'TEST_NAME': '<%= dbName %>_test',
                         'USER': '<%= dbUser %>',
                         'PASSWORD': get_env_setting('DB_PASSWORD'),
                         'HOST': '/var/run/mysqld/mysqld.sock', 'PORT': '',}}

MEDIA_ROOT = '/www/media'
STATIC_ROOT = '/www/static'
