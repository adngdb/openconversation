class Billets(object):
    '''Base class for lists of Billets. Needs to be extended. '''

    def get(self):
        '''Return a list of Billets. '''
        raise NotImplementedError
