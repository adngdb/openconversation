import requests

from openconversation.base import billet
from .base import MongoBase


class Billet(MongoBase, billet.Billet):

    def __init__(self, billet_id=None, data=None):
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

        if '_id' in data:
            self._id = data['_id']

    def save(self):
        data = dict((x, getattr(self, x)) for x in self.args)
        if self._id is not None:
            data['_id'] = self._id

        self._save(data)

    def get(self):
        '''Return a dictionary containing the data of this billet. '''
        return dict((x, getattr(self, x)) for x in self.args)

    def add_answer(self, answer_id):
        if not self.answers:
            self.answers = [answer_id]
        else:
            self.answers.append(answer_id)
        self.save()

    def _get(self, billet_id):
        '''Return a Billet's data from the mongodb database. '''
        with self.get_connection() as connection:
            return connection.billets.find_one({'billet_id': billet_id})

    def _save(self, data):
        '''Save a Billet into the mongodb database.

        If the Billet already exists, update it, otherwise create it.
        '''
        with self.get_connection() as connection:
            connection.billets.save(data)
