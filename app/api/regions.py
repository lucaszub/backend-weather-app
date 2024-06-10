from fastapi import APIRouter
from utils.query import Query
from database_singleton import DatabaseSingleton

router = APIRouter()

@router.get("/regions/")
async def get_regions():
    # Set the Blob Service URL

    query = Query()

    regions = query.get_distinct_regions()


    return {"Regions": regions}