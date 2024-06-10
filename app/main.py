from fastapi import FastAPI
from api.departements import router as departments_router  # Importez le routeur depuis le module departements
from api.regions import router as regions_router  # Importez le routeur depuis le module departements
from api.stations import router as stations_router  # Importez le routeur depuis le module departements
from api.year import router as year_router  # Importez le routeur depuis le module departements
from api.temperature_stat import router as temperature_stats_router  # Importez le routeur depuis le module temperature_stats
from fastapi.middleware.cors import CORSMiddleware
# Créer toutes les tables

origins = [
    "http://localhost:3000",  # Si votre front-end est servi sur localhost:3000
      # Si votre front-end est servi sur localhost:8000
]
app = FastAPI(
    title = f"Application météo API"
)

# Configuration du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(departments_router, prefix="/departments", tags=["departments"])  # Incluez le routeur dans votre application
app.include_router(regions_router, prefix="/regions", tags=["regions"])  # Incluez le routeur dans votre application
app.include_router(stations_router, prefix="/stations", tags=["stations"])  # Incluez le routeur dans votre application
app.include_router(year_router, prefix="/year", tags=["Year"])  # Incluez le routeur dans votre application
app.include_router(temperature_stats_router, prefix="/temperature_stats", tags=["temperature_stats"])  # Incluez le routeur dans votre application
@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather API"}