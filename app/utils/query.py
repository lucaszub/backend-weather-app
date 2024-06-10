from database_singleton import DatabaseSingleton
from model.temperature import Temperature 
from sqlalchemy import distinct

class Query():
    def __init__(self):
        self.session = DatabaseSingleton().session

    def get_distinct_regions(self):
        result = self.session.query(distinct(Temperature.region_name)).all()
        return [row[0] for row in result]

    def get_distinct_departments(self):
        result = self.session.query(distinct(Temperature.department_name)).all()
        return [row[0] for row in result]
    
    def get_distinct_id(self):
        result = self.session.query(distinct(Temperature.id_omm_station)).all()
        return [row[0] for row in result]
    
    def get_distinct_year(self):
        result = self.session.query(distinct(Temperature.year)).all()
        return [int(row[0]) for row in result]  # Convertir les valeurs en entiers

if __name__ == "__main__":
    query = Query()
    #print(query.get_distinct_regions())
    # print(query.get_distinct_departments())
    # print(query.get_distinct_year())
    print(query.get_distinct_id())