import pymongo

from . import Billet
from .base import MongoBase


class Billets(MongoBase):
    def get(self):
        '''Return all billets that are first level (answer to nothing), ordered
        by descending date. '''
        with self.get_connection() as connection:
            billets = connection.billets.find({
                'answer_to': None
            }).sort('date_created', -1)

            return [Billet(data=x) for x in billets]
