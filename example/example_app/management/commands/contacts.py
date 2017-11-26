import multiprocessing
from django import db
from django.core.management.base import BaseCommand
from example_app.models import Contact
from faker import Faker
import gc


fake = Faker()


DEFAULT_WORKERS = 4


def worker(args):
    db.connections.close_all()
    index = args
    page = index * 500
    contacts = []
    print('Creating Contacts {0} - {1}'.format(page, page + 500));
    for x in range(500):
        contacts.append(
            Contact(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                url=fake.url(),
                email=fake.email(),
                bio=fake.text(),
                birthday=fake.date_time()
            ))
    Contact.objects.bulk_create(contacts)
    gc.collect()


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.workers = options.get('workers', DEFAULT_WORKERS)
        pool = multiprocessing.Pool(self.workers)
        pool.map(worker, range(1000))
