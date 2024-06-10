import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
from datetime import datetime

def create_database(database_name):
    try:
        cnx = mysql.connector.connect(user='root', password='Medard44', host='localhost')
        cursor = cnx.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
    except Exception as e:
        print(f"Erreur lors de la création de la base de données {database_name} : {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals():
            cnx.close()

def process_data(chemin_fichier, colonnes): 
    df = pd.read_csv(chemin_fichier, sep=';', usecols=colonnes)

    # Supprimer les enregistrements des 10 stations avec NaN dans 'region (name)' et 'communes (name)'
    stations_to_drop = [61972, 61968, 61970, 89642, 61997, 71805, 61998, 61996, 61976, 78894]
    df = df[~df['ID OMM station'].isin(stations_to_drop)]

    regions_to_drop = ["Guyane", "Martinique", "Guadeloupe", "La Réunion", "Mayotte"] 
    df = df[~df['region (name)'].isin(regions_to_drop)]

    # Supprimer les lignes avec NaN dans 'Température (°C)'
    df = df.dropna(subset=['Température (°C)'])
        # Drop NaN values from the column 'Précipitations dans les 3 dernières heures'
    df = df.dropna(subset=['Précipitations dans les 3 dernières heures'])
    # Supprimer les lignes où 'Température maximale sur 12 heures (°C)' est supérieure à 50
    df = df[df['Température maximale sur 12 heures (°C)'] <= 50]

    # Remplir les NaN dans 'Température minimale sur 12 heures (°C)' avec les valeurs de 'Température (°C)'
    df['Température minimale sur 12 heures (°C)'] = df['Température minimale sur 12 heures (°C)'].fillna(df['Température (°C)'])

    # Remplir les NaN dans 'Température maximale sur 12 heures (°C)' avec les valeurs de 'Température (°C)'
    df['Température maximale sur 12 heures (°C)'] = df['Température maximale sur 12 heures (°C)'].fillna(df['Température (°C)'])

    # Convertir la colonne de date en format datetime
    df['Date'] = pd.to_datetime(df['Date'], utc=True)

    # Extraire l'année, le mois, le jour de la colonne 'Date'
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    # Grouper les données par 'ID OMM station', 'Year', 'Month' et 'Day' et calculer les agrégations
    grouped = df.groupby(['ID OMM station', 'Year', 'Month', 'Day']).agg({
        'Température (°C)': 'mean',
        'Température maximale sur 12 heures (°C)': 'max',
        'Température minimale sur 12 heures (°C)': 'min',
        'Précipitations dans les 3 dernières heures': 'sum',
        'Latitude': 'first',
        'Longitude': 'first',
        'department (name)': 'first',
        'region (name)': 'first',
        'communes (name)': 'first'
    }).reset_index()

    # Renommer les colonnes
    grouped = grouped.rename(columns={
        'Température (°C)': 'Temperature Moyenne',
        'Température maximale sur 12 heures (°C)': 'Temperature Maximale',
        'Température minimale sur 12 heures (°C)': 'Temperature Minimale',
        'Précipitations dans les 3 dernières heures': 'Precipitations',
    })

    # Arrondir la colonne "Température Moyenne" à un chiffre après la virgule
    grouped['Temperature Moyenne'] = grouped['Temperature Moyenne'].round(1)
    # Arrondir la colonne "Température Moyenne" à un chiffre après la virgule
    grouped['Temperature Maximale'] = grouped['Temperature Maximale'].round(1)

    grouped['Temperature Minimale'] = grouped['Temperature Minimale'].round(1)


    return grouped

# Colonnes à utiliser pour le traitement des données
colonnes = [
    'ID OMM station',
    'Date',
    'Température (°C)',
    'Température minimale sur 12 heures (°C)',
    'Température maximale sur 12 heures (°C)',
    'Précipitations dans les 3 dernières heures',
    'Latitude',
    'Longitude',
    'department (name)',
    'region (name)',
    'communes (name)'
]

csv_file_path = "C:\\wild code school\\weather_app\\backend weather app\\donnees-synop-essentielles-omm (4).csv"
# Traiter les données pour les températures moyennes, minimales et maximales
df_processed = process_data(csv_file_path, colonnes)

# Nom de la base de données MySQL
database_name = 'METEO_DATA'

# Créer la base de données si elle n'existe pas
create_database(database_name)

# Création de la connexion à la base de données MySQL (en spécifiant la base de données)
engine = create_engine(f'mysql+mysqlconnector://root:Medard44@localhost:3310/{database_name}')

# Charger les données de température moyenne dans la base de données MySQL
df_processed.to_sql('temperature', con=engine, if_exists='replace', index=False, chunksize=10000)

print("Chargement des données dans la base de données MySQL terminé avec succès.")
