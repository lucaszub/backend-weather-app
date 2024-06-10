from fastapi import APIRouter
from utils.query import Query

router = APIRouter()

@router.get("/regions/")
async def get_regions():
    # Set the Blob Service URL

    query = Query()

    stations = query.get_distinct_id()


    return {"Stations": stations}