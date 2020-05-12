from google.cloud import datastore


class DatastoreService:

    datastore_client = datastore.Client()

    def get(self, kind, filters):
        query = self.datastore_client.query(kind=kind)
        for key, value in filters.items():
            query.add_filter(key, '=', value)
        return list(query.fetch())

    def post(self, kind, key, exclude_from_indexes_tuple, values):
        entity = datastore.Entity(
            key=self.datastore_client.key(kind, key),
            # tuple with single value
            exclude_from_indexes=exclude_from_indexes_tuple)
        entity.update(values)
        self.datastore_client.put(entity)

    def delete(self, kind, key):
        self.datastore_client.delete(self.datastore_client.key(kind, key))
        print("deleting key " + key)


