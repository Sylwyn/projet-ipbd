#!/bin/bash

# Vérifier la présence du fichier .env
if [ ! -f .env ]; then
  echo ".env file not found!"
  exit 1
fi

# Extraire la première clé API du fichier .env
api_key=$(awk -F '"' '/^API_KEY_[A-Z]+/ {print $2; exit}' .env)

# Extraire tous les PUUID du fichier .env
puuids=$(awk -F '"' '/^PUUID_[A-Z]+/ {print $2}' .env)

# Vérifier la présence de la clé API et des PUUID
if [ -z "$api_key" ]; then
  echo "No API key found in .env!"
  exit 1
fi

if [ -z "$puuids" ]; then
  echo "No PUUIDs found in .env!"
  exit 1
fi

# Convertir les PUUID en tableau
puuids_array=($puuids)

counter=6938735500

# Utiliser la première clé API et parcourir chaque PUUID
for puuid in "${puuids_array[@]}"; do
    echo running ... $counter
    python3 scrap_incremental.py $api_key $puuid $counter 10000 &
    counter=$(($counter + 10000))
    sleep 2
done
