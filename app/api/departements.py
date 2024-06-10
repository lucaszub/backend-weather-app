from fastapi import APIRouter
from utils.query import Query
from database_singleton import DatabaseSingleton

router = APIRouter()

@router.get("/departements/")
async def get_departements():
    # Set the Blob Service URL

    query = Query()

    departements = query.get_distinct_departments()


    return {"departements": departements}