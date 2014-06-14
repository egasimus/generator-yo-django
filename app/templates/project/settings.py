import os, sys

if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
    print 'DJANGO_SETTINGS_MODULE not set'
    sys.exit(1)
