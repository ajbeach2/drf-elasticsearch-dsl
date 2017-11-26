import multiprocessing
from django import db
from drf_elasticsearch_dsl.connection_handler import connection_handler
from django.core.management.base import BaseCommand

DEFAULT_BATCH_SIZE = 500
DEFAULT_WORKERS = 4


def worker(args):
    document, model, start, end = args
    db.connections.close_all()
    row = model.objects.all()[start:end]
    document.bulk_index(row)
    db.reset_queries()


class Command(BaseCommand):
    help = "Freshens the index for the given app(s)."

    def handle(self, *args, **options):
        self.workers = 4  # options.get('workers', DEFAULT_WORKERS)
        self.batch_size = options.get('batch_size', DEFAULT_BATCH_SIZE)
        pool = multiprocessing.Pool(self.workers)
        queue = []

        for lablel, document in connection_handler.documents.items():
            model = document.get_model()
            qs = model.objects.all()

            total = qs.count()
            print('Indexing {0} records of {1}'.format(total, lablel))
            for start in range(0, total, self.batch_size):
                end = min(start + self.batch_size, total)
                queue.append((document, model, start, end))

        pool.map(worker, queue)
