# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
import os
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "mbb7o9l^03*a^5-b)0*y%8v*=p#p@wh+589i1n3-(@h-e7fz#4"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "drf_elasticsearch_dsl",


    "tests"
]

DRF_SERIALIZER_ELASTICSERACH_SETTTINGS = {
    'elasticsearch_hosts': ['localhost'],
}

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()
