from django.core.exceptions import ObjectDoesNotExist
import gc


def chunk_queryset_iterator(queryset, chunk_size=1000):
    """
    Iterate over a Django Queryset ordered by the primary key
    This method loads a maximum of chunk_size (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.
    Note that the implementation of the iterator does not support ordered query sets.
    """
    try:
        last_pk = queryset.order_by('-pk')[:1].get().pk
    except ObjectDoesNotExist:
        return

    pk = 0
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        row = queryset.filter(pk__gt=pk)[:chunk_size]
        pk = row.last().pk
        yield row
        gc.collect()
