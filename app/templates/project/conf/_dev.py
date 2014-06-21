from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )

DATABASES = {
    'default': {
        'NAME': '<%= dbName %>',
        'TEST_NAME': '<%= dbName %>_test',
        'USER': '<%= dbUser %>',
        'PASSWORD': get_env_setting('DB_PASSWORD'),
        <% if (dbType === 'mysql') { %>
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '/var/run/mysqld/mysqld.sock',
        'PORT': '',
        <% } %>
        <% if (dbType === 'postgres') { %>
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '/opt/run/pgsql',
        'PORT': '',
        <% } %>
        }}

MEDIA_ROOT = '/www/media'
STATIC_ROOT = '/www/static'
