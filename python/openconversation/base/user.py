class User(object):

    args = (
        'email',
        'is_admin',
    )

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def get(self):
        '''Return a dictionary containing the data of this User. '''
        raise NotImplementedError
