=============================
DRF Elasticsearch DSL
=============================

.. image:: https://badge.fury.io/py/drf-elasticsearch-dsl.svg
    :target: https://badge.fury.io/py/drf-elasticsearch-dsl

.. image:: https://circleci.com/gh/ajbeach2/drf-elasticsearch-dsl.svg?style=svg
    :target: https://circleci.com/gh/ajbeach2/drf-elasticsearch-dsl

.. image:: https://codecov.io/gh/ajbeach2/drf-elasticsearch-dsl/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ajbeach2/drf-elasticsearch-dsl

DRF Elasticsearch DSL is losely based on `django-haystack`_ and provides a ``ModelSerializerDocument``
which supports all of the field types provided by `elastic-search-dsl persistence`_. The library also optionall provides support for async document updates and deletes with `celery`_.

The purpose of this libraray is to allow definition of elasticsearch documents with DRF's `ModelSerializer`_ class and automatically sync documents to elasticsearch async with celery.

.. _`django-haystack`: https://github.com/django-haystack/django-haystack
.. _`elastic-search-dsl persistence`: http://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html
.. _`celery`: http://docs.celeryproject.org
.. _`ModelSerializer` : http://www.django-rest-framework.org/api-guide/serializers/#modelserializer

Documentation
-------------

The full documentation is at https://drf-elasticsearch-dsl.readthedocs.io.

Quickstart
----------

Install Django Package::

    pip install drf-elasticsearch-dsl

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'drf_elasticsearch_dsl.apps.DrfElasticsearchDsl',
        ...
    )

Create A model and serializer

.. code-block:: python

    class Contact(models.Model):
        first_name = models.CharField(max_length=32, null=False, blank=False)
        last_name = models.CharField(max_length=32, null=False, blank=False)
        url = models.URLField(null=False, blank=False)
        email = models.EmailField(max_length=254, null=False, blank=False)
        bio = models.TextField(null=False, blank=False)
        birthday = models.DateField(null=False, blank=False)


    from rest_framework import serializers

    class ContactSerializer(serializers.ModelSerializer):

        class Meta:
            model = Contact
            fields = '__all__'

Create A search_indexes.py in the root of the application.

.. code-block:: python

    from drf_elasticsearch_dsl.documents import ModelSerializerDocument
    from elasticsearch_dsl import Date, Keyword, Text, String
    from .serialziers import ContactSerializer


    class ContactSerializerDocument(ModelSerializerDocument):
        first_name = String()
        last_name = String()
        url = Keyword()
        email = Keyword()
        bio = Text()
        birthday = Date()

        class Meta:
            index = 'tests'
            serializer = ContactSerializer
            doc_type = 'tests.contact'



Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
