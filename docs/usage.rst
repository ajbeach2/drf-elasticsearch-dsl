=====
Usage
=====

To use Django Package in a project, add it to your `INSTALLED_APPS`:

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
