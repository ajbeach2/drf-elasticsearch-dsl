# -*- coding: utf-8 -*-

"""
test_drf-elasticsearch-dsl
------------

Tests for `drf-elasticsearch-dsl` models module.
"""

from django.test import TestCase
from drf_elasticsearch_dsl.tasks import (searchIndexUpdateTask,
                                         searchIndexDeleteTask)
from .models import Contact
from .serialziers import ContactSerializer
from .search_indexes import ContactSerializerDocument
from .factories import ContactFactory
from elasticsearch.exceptions import NotFoundError


class TestTasks(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.contact = ContactFactory.create()
        cls.contact.save()
        cls.expected = ContactSerializer(cls.contact).data
        super(TestTasks, cls).setUpClass()

    def test_tasks(self):
        searchIndexUpdateTask(Contact._meta.label_lower, self.contact.id)
        ContactSerializerDocument.refresh_index()
        contact = ContactSerializerDocument.get(self.contact.id)
        self.assertDictEqual(contact, self.expected)
        ContactSerializerDocument.refresh_index()
        searchIndexDeleteTask(Contact._meta.label_lower, self.contact.id)
        self.assertRaises(NotFoundError,
                          ContactSerializerDocument.get, self.contact.id)
