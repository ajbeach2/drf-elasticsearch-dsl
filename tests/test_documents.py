#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_drf-elasticsearch-dsl
------------

Tests for `drf-elasticsearch-dsl` models module.
"""

from django.test import TestCase

from .search_indexes import ContactSerializerDocument
from .serialziers import ContactSerializer
from .models import Contact
from .factories import ContactFactory


class TestDocuments(TestCase):

    def setUp(self):
        self.contact_doc = ContactSerializerDocument._doc_type
        self.label = Contact._meta.label_lower
        self.app_label = Contact._meta.app_label
        self.contact = ContactFactory.create()
        self.contact.save()

    def test_meta(self):
        self.assertEqual(self.contact_doc.index,
                         self.app_label)
        self.assertEqual(self.contact_doc.serializer,
                         ContactSerializer)
        self.assertEqual(self.contact_doc.doc_type,
                         self.label)
        self.assertEqual(ContactSerializerDocument.model_label,
                         self.label)

    def test_doc_type_options(self):
        self.assertEqual(self.contact_doc.model,
                         ContactSerializer.Meta.model)
        self.assertEqual(self.contact_doc.name,
                         self.label)

    def test_mapping(self):
        mapping = self.contact_doc.mapping
        self.assertEqual(mapping.properties.to_dict(), {
            'tests.contact': {
                'properties': {
                    'bio': {
                        'type': 'text'
                    },
                    'birthday': {
                        'type': 'date'
                    },
                    'email': {
                        'type': 'keyword'
                    },
                    'first_name': {
                        'type': 'string'
                    },
                    'last_name': {
                        'type': 'string'
                    },
                    'url': {
                        'type': 'keyword'
                    }
                }
            }
        })

    def tearDown(self):
        pass
