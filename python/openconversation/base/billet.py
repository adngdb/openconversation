class Billet(object):
    '''Base class for individual Billet. Needs to be extended. '''

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

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def save(self):
        '''Save this billet's data into a storage system. '''
        raise NotImplementedError

    def get(self):
        '''Return a dictionary containing the data of this billet. '''
        raise NotImplementedError

    def add_answer(self, answer_id):
        '''Add an answer to this Billet and save it. '''
        raise NotImplementedError
