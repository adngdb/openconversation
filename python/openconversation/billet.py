import pymongo

from .base import MongoBase


class Billet(MongoBase):
    args = (
        'billet_id',
        'content',
        'title',
        'tags',
        'author',
        'date_created',
        'answer_to',
        'answers',
    )

    def __init__(self, billet_id=None, data=None, config=None):
        self._id = None

        if billet_id is None and data is None:
            # This is a new, empty Billet. Nothing to do.
            return

        if billet_id is not None:
            data = self._get(billet_id)

        if not data:
            raise ValueError('Not found')

        for key in self.args:
            self.__setattr__(key, data.get(key))

        self._id = data['_id']

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def save(self):
        data = dict((x, getattr(self, x)) for x in self.args)
        if self._id is not None:
            data['_id'] = self._id

        self._save(data)

    def _get(self, billet_id):
        with self.get_connection() as connection:
            return connection.billets.find_one({'billet_id': billet_id})

    def _save(self, data):
        with self.get_connection() as connection:
            connection.billets.save(data)
