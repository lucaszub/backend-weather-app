from dotenv import load_dotenv
import os

# Charger les variables d'environnement du fichier .env
load_dotenv()

# Créer le dictionnaire de configuration de la base de données
database_config = dict()
database_config['username'] = os.getenv('DB_USERNAME')
database_config['password'] = os.getenv('DB_PASSWORD')
database_config['host'] = os.getenv('DB_HOST')
database_config['port'] = os.getenv('DB_PORT')
database_config['database'] = os.getenv('DB_NAME')

class dictToClass():
    def __init__(self,**kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)

database_config = dictToClass(**database_config)

if __name__=="__main__":
    print(database_config.password)