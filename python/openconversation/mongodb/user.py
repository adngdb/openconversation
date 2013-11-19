from openconversation.base import user
from .base import MongoBase


class User(MongoBase, user.User):

    def __init__(self, email):
        data = self.get(email)
        self.is_admin = data and 'is_admin' in data and data['is_admin']

    def get(self, email):
        with self.get_connection() as connection:
            return connection.users.find_one({'email': email})
