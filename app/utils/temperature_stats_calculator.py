from datetime import datetime
from utils.date_difference_calculator import DateDifferenceCalculator 
from database_singleton import DatabaseSingleton
from sqlalchemy import func
from model.temperature import Temperature
import calendar

class TemperatureStatsCalculator:
    def __init__(self, start_date_str, end_date_str, region_name=None, department_name=None):
        self.start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        self.region_name = region_name
        self.department_name = department_name
        self.session = DatabaseSingleton().session

    def calculate_stats(self, granularity):
        if granularity == 'jour':
            return self._calculate_daily_stats()
        elif granularity == 'mois':
            return self._calculate_monthly_stats()
        elif granularity == 'trimestre':
            return self._calculate_quarterly_stats()
        elif granularity == 'année':
            return self._calculate_yearly_stats()

    def _apply_filters(self, query):
        if self.region_name:
            query = query.filter(Temperature.region_name == self.region_name)
        if self.department_name:
            query = query.filter(Temperature.department_name == self.department_name)
        return query

    def _calculate_daily_stats(self):
        query = self.session.query(
            Temperature.year,
            Temperature.month,
            Temperature.day,
            func.round(func.avg(Temperature.temperature_moyenne), 1).label('temperature_moyenne'),
            func.min(Temperature.temperature_minimale).label('temperature_minimum'),
            func.max(Temperature.temperature_maximale).label('temperature_maximum')
        ).filter(
            (Temperature.year >= self.start_date.year) &
            (Temperature.year <= self.end_date.year) &
            (Temperature.month >= self.start_date.month) &
            (Temperature.month <= self.end_date.month)
        ).group_by(
            Temperature.year,
            Temperature.month,
            Temperature.day
        )
        query = self._apply_filters(query)
        result = query.all()
        return [row._asdict() for row in result]

    def _calculate_monthly_stats(self):
        query = self.session.query(
            Temperature.year,
            Temperature.month,
            func.round(func.avg(Temperature.temperature_moyenne), 1).label('temperature_moyenne'),
            func.round(func.min(Temperature.temperature_minimale), 1).label('temperature_minimum'),
            func.round(func.max(Temperature.temperature_maximale), 1).label('temperature_maximum')
        ).filter(
            (Temperature.year >= self.start_date.year) &
            (Temperature.year <= self.end_date.year) &
            (Temperature.month >= self.start_date.month) &
            (Temperature.month <= self.end_date.month)
        ).group_by(
            Temperature.year,
            Temperature.month
        )
        query = self._apply_filters(query)
        result = query.all()
        stats = [row._asdict() for row in result]

        # Convert month numbers to names
        for stat in stats:
            stat['month'] = calendar.month_name[stat['month']]

        return stats

    def _calculate_quarterly_stats(self):
        quarter_to_month = {
            1: 'January',
            2: 'April',
            3: 'July',
            4: 'October'
        }

        query = self.session.query(
            Temperature.year,
            ((Temperature.month - 1) // 3 + 1).label('quarter'),
            func.round(func.avg(Temperature.temperature_moyenne), 1).label('temperature_moyenne'),
            func.round(func.min(Temperature.temperature_minimale), 1).label('temperature_minimum'),
            func.round(func.max(Temperature.temperature_maximale), 1).label('temperature_maximum')
        ).filter(
            (Temperature.year >= self.start_date.year) &
            (Temperature.year <= self.end_date.year)
        ).group_by(
            Temperature.year,
            ((Temperature.month - 1) // 3 + 1)
        )
        query = self._apply_filters(query)
        result = query.all()

        # Convert the result to a list of dictionaries
        stats = []
        for row in result:
            stat_dict = {
                'quarter': quarter_to_month[row[1]] + ' ' + str(row[0]),  # Ajout de l'année en cours
                'temperature_moyenne': row[2],
                'temperature_minimum': row[3],
                'temperature_maximum': row[4]
            }
            stats.append(stat_dict)

        return stats

    def _calculate_yearly_stats(self):
        query = self.session.query(
            Temperature.year,
            func.round(func.avg(Temperature.temperature_moyenne), 1).label('temperature_moyenne'),
            func.round(func.min(Temperature.temperature_minimale), 1).label('temperature_minimum'),
            func.round(func.max(Temperature.temperature_maximale), 1).label('temperature_maximum')
        ).filter(
            (Temperature.year >= self.start_date.year) &
            (Temperature.year <= self.end_date.year)
        ).group_by(
            Temperature.year
        )
        query = self._apply_filters(query)
        result = query.all()
        return [row._asdict() for row in result]


if __name__ == "__main__":
    start_date_str = '2022-01-01'
    end_date_str = '2023-12-31'
    
    calculator = DateDifferenceCalculator(start_date_str, end_date_str)
    granularity = calculator.determine_granularity()
    
    Temperature_calculator = TemperatureStatsCalculator(start_date_str, end_date_str)
    stats = Temperature_calculator.calculate_stats(granularity)

    # Affichage des statistiques
    print("Statistiques:")
    for stat in stats:
        print(stat)
