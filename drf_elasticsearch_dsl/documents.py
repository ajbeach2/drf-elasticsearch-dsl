from elasticsearch_dsl import Search, Mapping, Field, Index
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from .helpers import chunk_queryset_iterator


DELETE_META_FIELDS = frozenset((
    'id', 'parent', 'routing', 'version', 'version_type'
))

DOC_META_FIELDS = frozenset((
    'timestamp', 'ttl'
)).union(DELETE_META_FIELDS)

META_FIELDS = frozenset((
    'index', 'using', 'score', 'doc_type', 'serializer'
)).union(DOC_META_FIELDS)


class MetaField(object):

    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs


class DocTypeOptions(object):

    def __init__(self, name, bases, attrs):
        meta = attrs.pop('Meta', None)
        self.meta = meta
        self.index = getattr(meta, 'index', None)
        self.doc_type = getattr(meta, 'doc_type', None)
        self._using = getattr(meta, 'using', None)
        self.mapping = getattr(meta, 'mapping', Mapping(self.doc_type))
        self.serializer = getattr(meta, 'serializer', None)

        for name, value in list(attrs.items()):
            if isinstance(value, Field):
                self.mapping.field(name, value)
                del attrs[name]

        for name in dir(meta):
            if isinstance(getattr(meta, name, None), MetaField):
                params = getattr(meta, name)
                self.mapping.meta(name, *params.args, **params.kwargs)

        for b in bases:
            if hasattr(b, '_doc_type') and hasattr(b._doc_type, 'mapping'):
                self.mapping.update(b._doc_type.mapping, update_only=True)
                self._using = self._using or b._doc_type._using
                self.index = self.index or b._doc_type.index

    @property
    def using(self):
        return self._using or 'default'

    @property
    def model(self):
        if not self.serializer:
            return None
        return self.serializer.Meta.model

    @property
    def name(self):
        return self.mapping.properties.name

    @property
    def parent(self):
        if '_parent' in self.mapping._meta:
            return self.mapping._meta['_parent']['type']
        return

    def resolve_field(self, field_path):
        return self.mapping.resolve_field(field_path)

    def init(self, index=None, using=None):
        self.mapping.save(index or self.index, using=using or self.using)

    def refresh(self, index=None, using=None):
        self.mapping.update_from_es(
            index or self.index, using=using or self.using)


class DocMeta(type):

    def __new__(cls, name, bases, attrs):
        attrs['_doc_type'] = DocTypeOptions(name, bases, attrs)
        model = attrs['_doc_type'].model
        if model is not None:
            attrs['model_label'] = model._meta.label_lower
        return type.__new__(cls, name, bases, attrs)


class ModelSerializerDocument(object, metaclass=DocMeta):
    use_for_search = True

    def __init__(self, instance, meta={}):
        self.instance = instance
        self.serializer = self._doc_type.serializer(instance)
        self.meta = meta
        self.meta["id"] = instance.pk

    @classmethod
    def get_model(cls):
        return cls._doc_type.model

    @classmethod
    def action_meta(cls, x):
        action = {}
        action["_type"] = cls._doc_type.doc_type
        action["_id"] = x["id"]
        action["_source"] = x
        return action

    @classmethod
    def bulk_index(cls, row=[]):
        es = connections.get_connection()
        items = cls._doc_type.serializer(row, many=True).data
        actions = list(map(cls.action_meta, items))
        success, _ = bulk(
            es, actions, index=cls._doc_type.index, raise_on_error=True)
        print('Performed %d actions' % success)

    @classmethod
    def bulk_index_queryset(cls, queryset=[]):
        es = connections.get_connection()

        for row in chunk_queryset_iterator(queryset):
            items = cls._doc_type.serializer(row, many=True).data
            actions = list(map(cls.action_meta, items))
            success, _ = bulk(
                es, actions, index=cls._doc_type.index, raise_on_error=True)
            print('Performed %d actions' % success)

    @classmethod
    def init(cls, index=None, using=None):
        cls._doc_type.init(index, using)

    @classmethod
    def get(cls, id, using=None, index=None, **kwargs):
        es = connections.get_connection(using or cls._doc_type.using)
        doc = es.get(
            index=index or cls._doc_type.index,
            doc_type=cls._doc_type.name,
            id=id,
            **kwargs
        )
        if not doc['found']:
            return None
        return doc["_source"]

    @classmethod
    def search(cls, using=None, index=None):
        return Search(
            using=using or cls._doc_type.using,
            index=index or cls._doc_type.index,
            doc_type=[cls._doc_type.doc_type]
        )

    @classmethod
    def refresh_index(cls):
        index = Index(cls._doc_type.index)
        return index.refresh()

    def _get_index(self, index=None):
        if index is None:
            index = getattr(self.meta, 'index', self._doc_type.index)
        if index is None:
            raise Exception('No index')
        return index

    def delete(self, using=None, index=None, **kwargs):
        es = connections.get_connection()
        doc_meta = dict(
            (k, self.meta[k])
            for k in DELETE_META_FIELDS
            if k in self.meta
        )

        doc_meta.update(kwargs)
        es.delete(
            index=self._get_index(),
            doc_type=self._doc_type.name,
            **doc_meta
        )

    def save(self, using=None, index=None, **kwargs):
        es = connections.get_connection()

        doc_meta = dict(
            (k, self.meta[k])
            for k in DOC_META_FIELDS
            if k in self.meta
        )
        doc_meta.update(kwargs)

        meta = es.index(
            index=self._get_index(),
            doc_type=self._doc_type.name,
            body=self.serializer.data,
            **doc_meta
        )

        return meta
