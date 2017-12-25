# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
import os
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "vx7b5S@Y)U&J_{&AGXc%&8uxc~y-$z>q<LpBhTR\F@%8y\Xyq`Y"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        'NAME': os.path.join(BASE_DIR, 'example_db.sqlite3'),
    }
}

ROOT_URLCONF = "example.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "drf_elasticsearch_dsl",


    "example_app",
    "django_celery_results",
]

CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

DRF_SERIALIZER_ELASTICSERACH_SETTTINGS = {
    'elasticsearch_hosts': ['localhost'],
    'signal_processor_class': 'drf_elasticsearch_dsl.signals.CelerySignalProcessor',
}

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()
