import contextlib
import pymongo

import settings


class MongoBase(object):

    @contextlib.contextmanager
    def get_connection(self):
        connection = pymongo.Connection(
            settings.DATABASE_HOSTNAME,
            settings.DATABASE_PORT
        )
        try:
            yield connection[settings.DATABASE_NAME]
        finally:
            connection.close()
