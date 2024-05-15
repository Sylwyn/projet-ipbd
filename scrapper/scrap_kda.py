###############################################################################################
# Code to scrap the kda of players in games by incrementing match_id                          #
# Typical usage is python3 scrap_kda.py api_key directory_name match_first_id number_of_match # 
# By default count = 100                                                                      #
###############################################################################################

import os
import sys
import time
import requests
import json

#get match data
def fetch_match_data(api_key, match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/EUW1_{match_id}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

#get kda of a given participant
def extract_kda(participant):
    kills = participant.get('kills', 0)
    deaths = participant.get('deaths', 0)
    assists = participant.get('assists', 0)
    kda = (kills + assists) / (deaths if deaths != 0 else 1)
    return kda

#save a given kda to a file
def save_kda_to_file(directory, match_id, kda_list):
    file_path = os.path.join(directory, f"{match_id}_kda.txt")
    with open(file_path, 'w') as file:
        for kda in kda_list:
            file.write(f"{kda}\n")

def main():
    #check usage
    if len(sys.argv) != 5:
        print("Usage: python3 scrap_kda.py api_key directory_name match_first_id number_of_match")
        sys.exit(1)
    
    #parameters
    api_key = sys.argv[1]
    directory_name = sys.argv[2]
    match_first_id = int(sys.argv[3])
    number_of_match = int(sys.argv[4])

    os.makedirs(directory_name, exist_ok=True)

    #through the match
    for i in range(number_of_match):
        match_id = match_first_id + i
        match_data = fetch_match_data(api_key, match_id)
        
        if not match_data:
            continue
        
        kda_list = [extract_kda(participant) for participant in match_data['info']['participants']]
        save_kda_to_file(directory_name, match_id, kda_list)

        # Control the request rate to not exceed 19 requests per second
        if (i + 1) % 19 == 0:
            time.sleep(1)
        else:
            time.sleep(0.05)  # Small sleep to slightly spread out the requests


if __name__ == "__main__":
    main()
