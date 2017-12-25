# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from drf_elasticsearch_dsl.urls import urlpatterns as drf_elasticsearch_dsl_urls

urlpatterns = [
    url(r'^', include('drf_elasticsearch_dsl.urls')),
]
