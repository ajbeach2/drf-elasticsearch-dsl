#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_drf-elasticsearch-dsl
------------

Tests for `drf-elasticsearch-dsl` connection_handler module.
"""

from django.test import TestCase
from drf_elasticsearch_dsl.connection_handler import connection_handler
from .search_indexes import *


class TestConnectionHandler(TestCase):

    def setUp(self):
        self.documents = connection_handler.documents
        self.contact_index = ContactSerializerDocument._doc_type.index

    def test_documents(self):
        self.assertEqual(self.documents[ContactSerializerDocument.model_label],
                         ContactSerializerDocument)

    def test_get_index(self):
        self.assertEqual(
            connection_handler.get_index(
                ContactSerializerDocument.model_label),
            ContactSerializerDocument)

    def tearDown(self):
        pass
