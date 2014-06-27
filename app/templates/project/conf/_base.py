from datetime import timedelta
import site

from django.utils.translation import ugettext_lazy as _

from . import rel, get_env_setting


# Add apps/ dir to import path, enabling us to use
# just 'import foo' in place of 'import apps.foo'
site.addpackage(rel(), "apps.pth", known_paths=set())


# Toggle debug mode
DEBUG = True
TEMPLATE_DEBUG = DEBUG


# Required by django.contrib.sites
SITE_ID = 1


# Caching
CACHES = {'default': {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
    'KEY_PREFIX': 'django-<%= projectName %>'}}
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = '<%= projectName %>:'
CACHE_HOMEPAGE = 20 * 1
CACHE_BSM = 60*60
CACHE_FEEDS = timedelta(minutes=60)


# Security
ALLOWED_HOSTS = ['<%= hostIP %>']
INTERNAL_IPS = ['127.0.0.1', '<%= hostIP %>']
SECRET_KEY = get_env_setting('SECRET_KEY')
ADMINS = ()
MANAGERS = ADMINS
# AUTH_USER_MODEL = 'cms_users.User'


# Locale
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y H:i'
TIME_FORMAT = 'H:i'
DATE_INPUT_FORMATS = ('%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', 
                      '%Y/%m/%d', '%Y-%m-%d',)
DATETIME_INPUT_FORMATS = ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%Y', 
                          '%d-%m-%Y %H:%M:%S', '%d-%m-%Y %H:%M', '%d-%m-%Y',
                          '%d.%m.%Y %H:%M:%S', '%d.%m.%Y %H:%M', '%d.%m.%Y',)
TIME_ZONE = 'Europe/London'


# Static and media
MEDIA_ROOT = ''
MEDIA_URL = '/media/'
SERVE_STATIC = DEBUG
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = [rel('static')]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',)
FILE_UPLOAD_PERMISSIONS = 0664


# Django infrastructure
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',)
TEMPLATE_DIRS = [rel('templates')]
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request")
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',)
WSGI_APPLICATION = 'wsgi.application'


# Apps
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'devserver',
    'south',
)


# Logging
loghandler = lambda f: {'class': 'logging.handlers.TimedRotatingFileHandler',
                        'level': 'DEBUG' if DEBUG else 'INFO',
                        'filename': '<%= logDir %>/' + f, 'backupCount': 7,
                        'when': 'midnight', 'interval': 1,
                        'formatter': 'main_formatter'}
LOG_FORMAT = ('%(asctime)s %(levelname)s :: %(name)s'
              ' :: %(message)s [%(filename)s:%(lineno)d]')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'},
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'}},

    'formatters': {
        'main_formatter': {'format': LOG_FORMAT,
                           'datefmt': "%Y-%m-%d %H:%M:%S"}},
    'handlers': {
        'null': {"class": 'django.utils.log.NullHandler'},
        'mail_admins': {'class': 'django.utils.log.AdminEmailHandler',
                        'level': 'ERROR', 'filters': ['require_debug_false']},
        'console': {'class': 'logging.StreamHandler', 'level': 'ERROR',
                    'formatter': 'main_formatter',
                    'filters': ['require_debug_true']},
        'app_log': loghandler('app.log'),
        'request_log': loghandler('request.log'),
        'db_log': loghandler('db.log')},

    'loggers': {
        'django.db.backends': {'handlers': ['db_log'],
                               'level': 'DEBUG', 'propagate': False},
        'django.request': {'handlers': ['request_log', 'mail_admins'],
                           'level': 'DEBUG', 'propagate': True},
        '': {'handlers': ['app_log', 'console'], 'level': 'DEBUG'}}}


# Urls
APPEND_SLASH = True
ROOT_URLCONF = '<%= projectName %>.urls'


# django-debug-toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False,
                        'SHOW_COLLAPSED': True}


# django-devserver
DEVSERVER_DEFAULT_ADDR = '0.0.0.0'
DEVSERVER_DEFAULT_PORT = '8000'
DEVSERVER_MODULES = (
    # 'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',
    'devserver.modules.ajax.AjaxDumpModule',
    # 'devserver.modules.profile.MemoryUseModule',
    'devserver.modules.cache.CacheSummaryModule',
    # 'devserver.modules.profile.LineProfilerModule',
)
