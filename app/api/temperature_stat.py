from fastapi import APIRouter, Query
from utils.temperature_stats_calculator import TemperatureStatsCalculator
from utils.date_difference_calculator import DateDifferenceCalculator

router = APIRouter()

@router.get("/temperature_stats/")
async def get_temperature_stats(start_date_str: str, end_date_str: str, 
                                region_name: str = Query(None), 
                                department_name: str = Query(None)):
    date_calculator = DateDifferenceCalculator(start_date_str, end_date_str)
    granularity = date_calculator.determine_granularity()

    temp_calculator = TemperatureStatsCalculator(start_date_str, end_date_str, region_name, department_name)
    stats = temp_calculator.calculate_stats(granularity)

    return {"temperature_stats": stats}