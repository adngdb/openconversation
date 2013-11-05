import pymongo

connection = pymongo.Connection()
db = connection.openconversation


class User(object):

    def __init__(self, email):
        data = self.get(email)
        self.isadmin = data and 'is_admin' in data and data['is_admin']

    def get(self, email):
        return db.users.find_one({'email': email})
