from database_config import database_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib import parse
from sqlalchemy import text

class database_connector():
    def __init__(self):
        self.engine = self.get_mysql_engine()
        self.session = sessionmaker(bind=self.engine)()

    def get_mysql_engine(self):
        connection_string = f"mysql+pymysql://{database_config.username}:{parse.quote_plus(database_config.password)}@{database_config.host}:{database_config.port}/{database_config.database}"
        return create_engine(connection_string)


#for testing
if __name__=="__main__":
    db_connector = database_connector()
    session = db_connector.session
    engine = db_connector.engine

    with engine.connect() as connection:
        result = connection.execution_options(isolation_level="AUTOCOMMIT").execute(text('SELECT * FROM temperature limit 10;'))
        for row in result:
            print(row)