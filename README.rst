=============================
DRF Elasticsearch DSL
=============================

.. image:: https://badge.fury.io/py/drf-elasticsearch-dsl.svg
    :target: https://badge.fury.io/py/drf-elasticsearch-dsl

.. image:: https://circleci.com/gh/ajbeach2/drf-elasticsearch-dsl.svg?style=svg
    :target: https://circleci.com/gh/ajbeach2/drf-elasticsearch-dsl

.. image:: https://codecov.io/gh/ajbeach2/drf-elasticsearch-dsl/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ajbeach2/drf-elasticsearch-dsl

Your project description goes here

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
        'drf_elasticsearch_dsl.apps.DjPackageConfig',
        ...
    )

Add Django Package's URL patterns:

.. code-block:: python

    from drf_elasticsearch_dsl import urls as drf_elasticsearch_dsl_urls


    urlpatterns = [
        ...
        url(r'^', include(drf_elasticsearch_dsl_urls)),
        ...
    ]

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
