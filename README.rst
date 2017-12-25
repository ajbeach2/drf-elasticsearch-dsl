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
which supports all of the field types provided by `elastic-search-dsl persistence`_.. ``ModelSerializerDocument`` is losely based of of the ``DocType`` class provided by ``elasticsearch-dsl.py``

The purpose of this libraray is to allow definition of elasticsearch documents with DRF's `ModelSerializer`_ class while optionally providing support for async document updates and deletes with `celery`_.



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


Configure DRF_SERIALIZER_ELASTICSERACH_SETTTINGS in your settings.py file with your elasticsearch url(s)

.. code-block:: python

    DRF_SERIALIZER_ELASTICSERACH_SETTTINGS = {
        'elasticsearch_hosts': ['localhost']
    }


Create a Model

.. code-block:: python

    from django.db import models


    class Contact(models.Model):

        first_name = models.CharField(max_length=32, null=False, blank=False)
        last_name = models.CharField(max_length=32, null=False, blank=False)
        url = models.URLField(null=False, blank=False)
        email = models.EmailField(max_length=254, null=False, blank=False)
        bio = models.TextField(null=False, blank=False)
        birthday = models.DateField(null=False, blank=False)


Create a ModelSerializer

.. code-block:: python

    from rest_framework import serializers

    class ContactSerializer(serializers.ModelSerializer):

        class Meta:
            model = Contact
            fields = '__all__'

Create a ``search_indexes.py``, which should be in the root of the application. Add your ``ModelSerializerDocument`` classes here. The specificed index will have its mapping updated for this document.

Note: Elasticsearch has removed support for mapping types.


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
            index = 'myapp'
            serializer = ContactSerializer
            doc_type = 'myapp.contact'

Finally, sync your database with elasticsearch by running:

::

    $ python manage.py update_index


Features
--------

Celery Support
==============

By default, dr-elasticsearch-dsl does not setup signals to sync models on save or delete. To enable celery support, add the following to your settings.py confiration:

.. code-block:: python

    DRF_SERIALIZER_ELASTICSERACH_SETTTINGS = {
        ...
        'signal_processor_class': 'drf_elasticsearch_dsl.signals.CelerySignalProcessor',
    }


See the `celery`_ documentation for details setting up celery with django

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ tox


TODO:
-----

- Add search URLS to be automatically added to all ``ModelSerializerDocument`` added to ``search_indexes.py``
- Better documentation
- Better test coverage

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
.. _`django-haystack`: https://github.com/django-haystack/django-haystack
.. _`elastic-search-dsl persistence`: http://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html
.. _`celery`: http://docs.celeryproject.org
.. _`ModelSerializer` : http://www.django-rest-framework.org/api-guide/serializers/#modelserializer

