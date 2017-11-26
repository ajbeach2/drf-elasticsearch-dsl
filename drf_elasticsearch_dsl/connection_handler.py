from django.utils.module_loading import module_has_submodule
from django.apps import apps
import importlib
import inspect


class ConnectionHandler(object):

    def __init__(self):
        self._documents = self.collect_documents()

    def get_index(self, label):
        return self.documents[label]

    @property
    def documents(self):
        return self._documents

    def collect_documents(self):
        documents = {}

        for app_mod in [i.module for i in apps.get_app_configs()]:
            try:
                search_index_module = importlib.import_module(
                    "%s.search_indexes" % app_mod.__name__)
            except ImportError:
                if module_has_submodule(app_mod, 'search_indexes'):
                    raise
                continue

            members = inspect.getmembers(search_index_module, inspect.isclass)
            for item_name, item in members:
                model_label = getattr(item, 'model_label', None)
                if getattr(item, 'use_for_search', False) and model_label:
                    documents[model_label] = item

        return documents


connection_handler = ConnectionHandler()
