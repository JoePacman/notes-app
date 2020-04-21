from google.cloud import datastore

datastore_client = datastore.Client()


def get(kind, filters):
    query = datastore_client.query(kind=kind)
    for key, value in filters.items():
        query.add_filter(key, '=', value)
    return list(query.fetch())


def post(kind, key, exclude_from_indexes_tuple, values):
    entity = datastore.Entity(
        key=datastore_client.key(kind, key),
        # tuple with single value
        exclude_from_indexes=exclude_from_indexes_tuple)
    entity.update(values)
    datastore_client.put(entity)


def delete(kind, key):
    datastore_client.delete(datastore_client.key(kind, key))


