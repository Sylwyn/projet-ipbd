##############################################################################################
# Code to scrap the full JSON of several games of a given Lol account                        #
# Typical usage is python3 scrap_user.py api_key directory_name puuid type start [count]     # 
# By default count = 100                                                                     #
##############################################################################################

import os
import sys
import time
import requests
import json

#get count games of the player puuid from game number start, in the type match_type
def fetch_match_ids(api_key, puuid, match_type, start, count):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type={match_type}&start={start}&count={count}&api_key={api_key}"
    print(f"Fetching match IDs with URL: {url}")  # Debug: Afficher l'URL de la requête
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch match IDs: {response.status_code} - {response.text}")
        return []

#get the data of the match with the id match_id
def fetch_match_data(api_key, match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch match data for {match_id}: {response.status_code} - {response.text}")
        return None

#save the entire JSON data to a file
def save_json_to_file(directory, match_id, json_data):
    file_path = os.path.join(directory, f"{match_id}.json")
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

def main():
    #check usage
    if len(sys.argv) < 6 or len(sys.argv) > 7:
        print("Usage: python3 scrap_full_json.py api_key directory_name puuid type [count]")
        sys.exit(1)
    
    #parameters
    api_key = sys.argv[1]
    directory_name = sys.argv[2]
    puuid = sys.argv[3]
    match_type = sys.argv[4]
    start = sys.argv[5]
    count = 100 if len(sys.argv) == 6 else int(sys.argv[6])

    #if you send more than 100 requests api does not work
    if count > 100:
        print("Error: count cannot be greater than 100")
        sys.exit(1)

    os.makedirs(directory_name, exist_ok=True)

    
    match_ids = fetch_match_ids(api_key, puuid, match_type, start, count)
    time.sleep(6)
    #through every match
    for idx, match_id in enumerate(match_ids):
        match_data = fetch_match_data(api_key, match_id)
        if not match_data:
            continue
        
        save_json_to_file(directory_name, match_id, match_data)

        # Control the request rate to not exceed 19 requests per second 
        time.sleep(2) 


if __name__ == "__main__":
    main()
