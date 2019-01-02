""" Define Database (factory class & DBInterface to handle CRUD  """
from sqlalchemy import create_engine


class Database():
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        'sqlite': 'sqlite:///{DB}',
    }

    # Main DB connection reference object
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=':memory:'):
        """ Create database engine based on given parameters """
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")


# TODO: create DB_Interface