from django.apps import apps
from celery import shared_task
from celery.utils.log import get_task_logger
from drf_elasticsearch_dsl.connection_handler import connection_handler

logger = get_task_logger(__name__)


@shared_task(bind=True)
def searchIndexUpdateTask(self, app_label, model_name, pk, using):
    try:
        model_class = apps.get_model(app_label, model_name)
        instance = model_class.objects.get(pk=pk)
        indexer = connection_handler.get_index(model_class)
        serializer_class = indexer["serializer"]
        index_class = indexer["index"]
        data = serializer_class(instance)
        doc = index_class(data)
        doc.save()

    except Exception as exc:
        logger.exception(exc)
        self.retry(exc=exc, max_retries=5, countdown=30)


@shared_task(bind=True)
def searchIndexDeleteTask(self, app_label, model_name, pk, using):
    try:
        model_class = apps.get_model(app_label, model_name)
        indexer = connection_handler.get_index(model_class)
        index_class = indexer["index"]
        indexer = index_class({id: pk})
        indexer.delete()

    except Exception as exc:
        logger.exception(exc)
        self.retry(exc=exc, max_retries=5, countdown=30)
