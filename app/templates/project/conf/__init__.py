#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from os.path import pardir, dirname
absjoin = lambda *args: os.path.abspath(os.path.join(*args))
DJANGO_ROOT = absjoin(dirname(__file__), pardir)


def rel(*path):
    """
    Converts path relative to the project root into an absolute path

    :rtype: str
    """
    return absjoin(DJANGO_ROOT, *path).replace("\\", "/")


def get_env_setting(setting):
    """
    Get the environment setting or raise exception

    :rtype: str
    """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        print("Error:" + error_msg)
        # TODO: the error below is somehow caught and doesn't show in the
        # output that it failed.
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(error_msg)


