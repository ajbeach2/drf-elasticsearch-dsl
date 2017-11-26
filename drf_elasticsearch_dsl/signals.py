from django.db import models
from .tasks import searchIndexUpdateTask, searchIndexDeleteTask
from drf_elasticsearch_dsl.connection_handler import connection_handler


class CelerySignalProcessor(object):

    def __init__(self):
        self.setup()

    def handle_save(self, sender, instance, **kwargs):
        pass
        # raw = kwargs.get('raw', False)
        # if not raw:
        #     meta = instance._meta
        #     searchIndexUpdateTask.delay(
        #         meta.app_label, meta.model_name, instance.pk)

    def handle_delete(self, sender, instance, **kwargs):
        pass
        # raw = kwargs.get('raw', False)
        # if not raw:
        #     meta = instance._meta
        #     searchIndexDeleteTask.delay(
        #         meta.app_label, meta.model_name, instance.pk)

    def setup(self):
        pass
        # for lablel, document in connection_handler.documents:
        #     model = document.get_model()
        #     model.signals.post_save.connect(
        #         self.handle_save, sender=model
        #     )
        #     models.signals.post_delete.connect(
        #         self.handle_delete, sender=model
        #     )

    def teardown(self):
        pass
        # for lablel, document in connection_handler.documents:
        #     model = document.get_model()
        #     model.signals.post_save.disconnect(
        #         self.handle_save, sender=model
        #     )
        #     models.signals.post_delete.disconnect(
        #         self.handle_delete, sender=model
        #     )
