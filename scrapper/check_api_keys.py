import os
import subprocess
import shutil
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Extraire les clés API qui commencent par 'API_KEY_'
api_keys = {key: value for key, value in os.environ.items() if key.startswith('API_KEY_')}

# Extraire le PUUID de Wozis
wozis_puuid = os.getenv("Wozis_PUUID")
# Paramètres communs pour le script principal
directory_name = "output_directory"
match_type = "ranked"
count = "1"  # vous pouvez ajuster le nombre de jeux ici

# Fonction pour exécuter le script principal avec une clé API donnée et le puuid de Wozis
def run_script(api_key, puuid):
    try:
        result = subprocess.run(
            ["python3", "scrap_user.py", api_key, directory_name, puuid, match_type, count],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True  # Remplacer text=True par universal_newlines=True
        )
        print(f"{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error with {key} : {e.stderr}")

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(directory_name, exist_ok=True)

# Tester chaque clé API avec le PUUID de Wozis
for key, api_key in api_keys.items():
    print(f"Testing {key}")
    run_script(api_key, wozis_puuid)

# Supprimer le dossier de sortie à la fin
shutil.rmtree(directory_name)
print(f"Deleted directory: {directory_name}")
