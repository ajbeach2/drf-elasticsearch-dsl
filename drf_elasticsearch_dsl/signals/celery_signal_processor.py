from drf_elasticsearch_dsl.tasks import searchIndexUpdateTask, searchIndexDeleteTask
from drf_elasticsearch_dsl.connection_handler import connection_handler
from django.db.models.signals import post_delete, post_save


class CelerySignalProcessor(object):

    def __init__(self):
        self.setup()

    def handle_save(self, sender, instance, **kwargs):
        raw = kwargs.get('raw', False)
        if not raw:
            meta = instance._meta
            searchIndexUpdateTask.delay(
                meta.label, instance.pk)

    def handle_delete(self, sender, instance, **kwargs):
        raw = kwargs.get('raw', False)
        if not raw:
            meta = instance._meta
            searchIndexDeleteTask.delay(
                meta.lable, instance.pk)

    def setup(self):
        for lablel, document in connection_handler.documents.items():
            model = document.get_model()
            post_save.connect(
                self.handle_save, sender=model
            )
            post_delete.connect(
                self.handle_delete, sender=model
            )

    def teardown(self):
        for lablel, document in connection_handler.documents.items():
            model = document.get_model()
            post_save.disconnect(
                self.handle_save, sender=model
            )
            post_delete.disconnect(
                self.handle_delete, sender=model
            )
