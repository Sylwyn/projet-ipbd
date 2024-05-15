#######################################################################################################
# Code to scrap the entire JSON of games by incrementing match_id                                     #
# Typical usage is python3 scrap_incremental.py api_key directory_name match_first_id number_of_match #                                                                          #
#######################################################################################################

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

#save the entire JSON data to a file
def save_json_to_file(directory, match_id, json_data):
    file_path = os.path.join(directory, f"{match_id}.json")
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

def main():
    #check usage
    if len(sys.argv) != 5:
        print("Usage: python3 scrap_json.py api_key directory_name match_first_id number_of_match")
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
            #print(f"Failed to download match ID {match_id} or empty response")
            continue
        
        save_json_to_file(directory_name, match_id, match_data)

        # Control the request rate to not exceed 19 requests per second
        time.sleep(2)  # Sleep for 1.2 seconds between requests

if __name__ == "__main__":
    main()
