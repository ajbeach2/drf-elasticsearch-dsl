# -*- coding: utf-8
from django.apps import AppConfig
from django.conf import settings
from elasticsearch_dsl.connections import connections
from django.core.exceptions import ImproperlyConfigured


class DrfElasticsearchDsl(AppConfig):
    name = 'drf_elasticsearch_dsl'

    def ready(self):
        from .signals import CelerySignalProcessor
        from .connection_handler import connection_handler

        self.drf_elasticsearch_dsl_settings = getattr(
            settings,
            'DRF_SERIALIZER_ELASTICSERACH_SETTTINGS', None)

        if self.drf_elasticsearch_dsl_settings is None:
            raise ImproperlyConfigured(
                'DRF_SERIALIZER_ELASTICSERACH_SETTTINGS is missing from settings')

        self.elasticsearch_hosts = self.drf_elasticsearch_dsl_settings.get(
            'elasticsearch_hosts', None)

        if self.elasticsearch_hosts is None:
            raise ImproperlyConfigured(
                'DRF_SERIALIZER_ELASTICSERACH_SETTTINGS is missing elasticsearch_hosts')

        connections.create_connection(hosts=self.elasticsearch_hosts)
        self.connection_handler = connection_handler
        self.signal_processor = CelerySignalProcessor()
