from drf_elasticsearch_dsl.documents import ModelSerializerDocument
from elasticsearch_dsl import Date, Keyword, Text, String
from .serialziers import ContactSerializer


class ContactSerializerDocument(ModelSerializerDocument):
    first_name = String()
    last_name = String()
    url = Keyword()
    email = Keyword()
    bio = Text()
    birthday = Date()

    class Meta:
        index = 'tests'
        serializer = ContactSerializer
        doc_type = 'tests.contact'
