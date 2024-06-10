from datetime import datetime

class DateDifferenceCalculator:
    def __init__(self, start_date_str, end_date_str):
        self.start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    def calculate_differences(self):
        if self.start_date is None or self.end_date is None:
            raise ValueError("Les dates de début et de fin doivent être définies avant de calculer les différences.")
        
        delta = self.end_date - self.start_date
        days = delta.days
        months = self._calculate_months()
        quarters = self._calculate_quarters(months)
        years = months // 12
        
        return {
            "days": days,
            "months": months,
            "quarters": quarters,
            "years": years
        }

    def determine_granularity(self):
        differences = self.calculate_differences()
        days = differences['days']
        
        if days < 31:
            granularity = 'jour'
        elif days < 365:
            granularity = 'mois'
        elif days < 3 * 365:
            granularity = 'trimestre'
        else:
            granularity = 'année'
        
        return granularity

    def _calculate_months(self):
        return (self.end_date.year - self.start_date.year) * 12 + self.end_date.month - self.start_date.month

    def _calculate_quarters(self, months):
        quarter_to_month = {
            1: 'Janvier',
            2: 'Avril',
            3: 'Juillet',
            4: 'Octobre'
        }
        return quarter_to_month[(self.start_date.month - 1) // 3 + 1]

    def display_differences(self, differences, granularity):
        print(f"Nombre de jours: {differences['days']}")
        print(f"Nombre de mois: {differences['months']}")
        if granularity == 'trimestre':
            print(f"Premier mois du trimestre: {differences['quarters']}")
        else:
            print(f"Nombre de trimestres: {differences['quarters']}")
        print(f"Nombre d'années: {differences['years']}")
        print(f"Granularité recommandée : par {granularity}")

# Utilisation de la classe avec des dates en dur
if __name__ == "__main__":
    start_date_str = '2021-12-01'
    end_date_str = '2022-12-31'
    
    calculator = DateDifferenceCalculator(start_date_str, end_date_str)
    differences = calculator.calculate_differences()
    granularity = calculator.determine_granularity()
    calculator.display_differences(differences, granularity)
