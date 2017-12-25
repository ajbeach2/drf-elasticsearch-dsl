from django.apps import apps
from celery import shared_task
from celery.utils.log import get_task_logger
from drf_elasticsearch_dsl.connection_handler import connection_handler

logger = get_task_logger(__name__)


@shared_task(bind=True)
def searchIndexUpdateTask(self, label, pk):
    try:
        model_class = apps.get_model(label)
        instance = model_class.objects.get(pk=pk)

        doc_class = connection_handler.get_index(label)
        doc = doc_class(instance)
        doc.save()

    except Exception as exc:
        logger.exception(exc)
        self.retry(exc=exc, max_retries=5, countdown=30)


@shared_task(bind=True)
def searchIndexDeleteTask(self, label, pk):
    try:
        model_class = apps.get_model(label)
        instance = model_class.objects.get(pk=pk)

        doc_class = connection_handler.get_index(label)
        doc = doc_class(instance)
        doc.delete()

    except Exception as exc:
        logger.exception(exc)
        self.retry(exc=exc, max_retries=5, countdown=30)
