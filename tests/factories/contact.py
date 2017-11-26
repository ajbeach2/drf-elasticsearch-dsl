import multiprocessing
from django import db
from tests.models import Contact
from faker import Faker
import gc

fake = Faker()
DEFAULT_PAGE = 200


def worker(args):
    db.connections.close_all()
    contacts = []
    for x in range(DEFAULT_PAGE):
        contacts.append(
            Contact(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                url=fake.url(),
                email=fake.email(),
                bio=fake.text(),
                birthday=fake.date()
            ))
    Contact.objects.bulk_create(contacts)
    gc.collect()


class ContactFactory(object):
    @classmethod
    def create(cls):
        return Contact(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            url=fake.url(),
            email=fake.email(),
            bio=fake.text(),
            birthday=fake.date()
        )

    @classmethod
    def bulk_insert(cls, workers=4, total=1000):
        pool = multiprocessing.Pool(workers)
        pool.map(worker, range(total))
