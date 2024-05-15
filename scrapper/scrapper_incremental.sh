#!/bin/bash

# Vérifier la liste des clés
if [ -f list_key ]; then
 	echo	start scrap
else
  echo "list_key file not found!"
  exit 1
fi

counter=6938735500
# Parcourir chaque clé d'API
for api_key in $( awk -F '"' '/^API_KEY_[A-Z]+/ {print $2}' .env) ; do
    echo running ... $counter
    python3 scrap_incremental.py $api_key random_data $counter 10000 &
    counter=$(($counter+10000))
    sleep 2
done
