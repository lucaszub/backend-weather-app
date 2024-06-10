from database_connector import database_connector
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# from models.T_IMMATRICULATION_AGREGEE import T_IMMATRICULATION_AGREGEE


class DatabaseSingleton:
    _instance = None
    _session = None
    _engine = None
    '''
    DatabaseSingleton is a singleton class that will be used to get the session object
    It prevents from creating multiple sessions and thus multiple connections to the database
    It can be used like this:
    
    from utils.database_singleton import DatabaseSingleton
from sqlalchemy.exc import SQLAlchemyError
    session = DatabaseSingleton().session
    
    now, session is a session object that can be used to query the database
    even if it used in multiple files, it will be the same session object
    '''''
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        obj = database_connector()
        self._session = obj.session
        self._engine = obj.engine

    def new_session(self):
        # Create a new session and engine without calling itself
        obj = database_connector()
        self._session = obj.session
        self._engine = obj.engine

    @property
    def session(self):
        return self._session

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._session

    @property
    def engine(self):
        return self._engine


if __name__ == "__main__":
    db = DatabaseSingleton()
    session = db.session

    try:
        result = session.execute(text('SELECT * FROM temperature LIMIT 10;'))
        for row in result:
            print(row)
        # Print column names
        print(result.keys())
    except SQLAlchemyError as e:
        print(f"An error occurred while executing the query: {e}")
    finally:
        session.close()