from .base import MongoBase


class User(MongoBase):

    def __init__(self, email):
        data = self.get(email)
        self.isadmin = data and 'is_admin' in data and data['is_admin']

    def get(self, email):
        with self.get_connection() as connection:
            return connection.users.find_one({'email': email})
