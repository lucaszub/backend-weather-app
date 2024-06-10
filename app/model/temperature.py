from sqlalchemy import Column, Integer, Float, String, BigInteger, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker
from database_singleton import DatabaseSingleton
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class Temperature(Base):
    __tablename__ = 'temperature'

    id_omm_station = Column('ID OMM station', BigInteger, primary_key=True)
    year = Column('Year', Integer)
    month = Column('Month', Integer)
    day = Column('Day', Integer)
    temperature_moyenne = Column('Temperature Moyenne', Float)
    temperature_maximale = Column('Temperature Maximale', Float)
    temperature_minimale = Column('Temperature Minimale', Float)
    latitude = Column('Latitude', Float)
    longitude = Column('Longitude', Float)
    department_name = Column('department (name)', String)
    region_name = Column('region (name)', String)
    communes_name = Column('communes (name)', String)

if __name__ == "__main__":
    # Initialize DatabaseSingleton
     # Initialize DatabaseSingleton
    db = DatabaseSingleton().session

    try:
        result = db.query(Temperature.year, 
                          Temperature.temperature_moyenne, 
                          Temperature.temperature_maximale, 
                          Temperature.temperature_minimale).limit(10).all()
        for row in result:
            print(row)
    except SQLAlchemyError as e:
        print(f"An error occurred while executing the query: {e}")
    finally:
        db.close()