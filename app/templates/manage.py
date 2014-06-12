#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
        print 'DJANGO_SETTINGS_MODULE not set'
        sys.exit(1)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
