import requests

from openconversation.base import billet


class InvalidActionError(Exception):
    pass


class Billet(billet.Billet):

    def __init__(self, billet_id):
        self._url = billet_id

        if billet_id is not None:
            data = self._get(billet_id)

        if not data:
            raise ValueError('Not found')

        for key in self.args:
            self.__setattr__(key, data.get(key))

    def save(self):
        raise InvalidActionError('Impossible to save a distant resource. ')

    def get(self):
        '''Return a dictionary containing the data of this billet. '''
        return dict((x, getattr(self, x)) for x in self.args)

    def add_answer(self, answer_id):
        payload = {'answer_id': answer_id}
        requests.post(self._url, params=payload)

    def _get(self, billet_id):
        '''Return a Billet's data from an external resource. '''
        # get from the network
        headers = {'content-type': 'application/json'}
        r = requests.get(billet_id, headers=headers)
        return r.json()
