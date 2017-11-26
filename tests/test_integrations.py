#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_drf-elasticsearch-dsl
------------

Tests for `drf-elasticsearch-dsl` models module.
"""

from django.test import TestCase

from .search_indexes import ContactSerializerDocument
from .factories import ContactFactory


class TestIntegrations(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.contact = ContactFactory.create()
        cls.contact.save()
        cls.contact_doc = ContactSerializerDocument(cls.contact)
        cls.success = cls.contact_doc.save()
        super(TestIntegrations, cls).setUpClass()

    def test_get(self):
        response = ContactSerializerDocument.get(id=self.contact.pk)
        serializer = ContactSerializerDocument._doc_type.serializer
        contact_data = serializer(self.contact).data
        self.assertEqual(response, contact_data)

    def test_search(self):
        s = ContactSerializerDocument.search()
        s.filter("term", email=self.contact.email)
        response = s.execute()
        for hit in response.hits:
            self.assertEqual(hit.to_dict()["email"], self.contact.email)

    @classmethod
    def tearDownClass(cls):
        cls.contact_doc.delete()
        super(TestIntegrations, cls).tearDownClass()
