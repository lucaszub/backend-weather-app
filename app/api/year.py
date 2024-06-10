from fastapi import APIRouter
from utils.query import Query

router = APIRouter()

@router.get("/Year/")
async def get_regions():
    # Set the Blob Service URL

    query = Query()

    Year = query.get_distinct_year()


    return {"Year": Year}