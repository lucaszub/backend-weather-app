uvicorn app.main:app --reload

docker exec -it mysql_container mysql -u root -p

USE METEO_DATA;

SELECT * FROM temperature LIMIT 10;

SELECT COUNT(*) FROM temperature;



Granularité par jour :

Si la période sélectionnée est inférieure à un mois (par exemple, moins de 31 jours), choisissez la granularité par jour. Cela permettra d'avoir une vue détaillée des variations quotidiennes.
Granularité par mois :

Si la période sélectionnée est d'au moins un mois mais inférieure à un an (par exemple, plus de 31 jours mais moins de 365 jours), choisissez la granularité par mois. Cela permettra d'observer les tendances mensuelles sans sacrifier trop de détails.
Granularité par trimestre :

Si la période sélectionnée est d'au moins un an mais inférieure à trois ans (par exemple, plus de 365 jours mais moins de 3 ans), choisissez la granularité par trimestre. Cela permettra de capturer les variations saisonnières sur des intervalles plus longs.
Granularité par année :

Si la période sélectionnée est de trois ans ou plus, choisissez la granularité par année. Cela fournira une vue d'ensemble des tendances annuelles sans surcharger le graphique avec trop de détails.