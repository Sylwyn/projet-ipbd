###################################################################################
# Code to scrap win or lose from an League of Legends account                     #
# Typical usage is python3 scrap_win.py api_key directory_name puuid type [count] # 
# By default count = 100                                                          #
###################################################################################

import os
import sys
import time
import requests
import json

# get count games of the player puuid from game number start, in the type match_type
def fetch_match_ids(api_key, puuid, match_type, start, count):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type={match_type}&start={start}&count={count}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch match IDs: {response.status_code} - {response.text}")
        return []

# get the data of the match with the id match_id
def fetch_match_data(api_key, match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch match data for {match_id}: {response.status_code} - {response.text}")
        return None

# get the status (win or lose) of player puuid in the game linked 
def extract_win_status(participants, puuid):
    for participant in participants:
        if participant['puuid'] == puuid:
            return participant['win']
    return None

# save a status in a file
def save_win_status_to_file(directory, match_id, win_status):
    file_path = os.path.join(directory, f"{match_id}_win.txt")
    with open(file_path, 'w') as file:
        file.write(f"{win_status}\n")

def main():
    # check usage
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print("Usage: python3 scrap_win.py api_key directory_name puuid type [count]")
        sys.exit(1)
    
    # parameters
    api_key = sys.argv[1]
    directory_name = sys.argv[2]
    puuid = sys.argv[3]
    match_type = sys.argv[4]
    start = 0
    count = 100 if len(sys.argv) == 5 else int(sys.argv[5])

    # if you send more than 100 requests api does not work
    if count > 100:
        print("Error: count cannot be greater than 100")
        sys.exit(1)

    os.makedirs(directory_name, exist_ok=True)

    match_ids = fetch_match_ids(api_key, puuid, match_type, start, count)
    
    # through every match
    for idx, match_id in enumerate(match_ids):
        match_data = fetch_match_data(api_key, match_id)
        
        if not match_data:
            continue
        
        win_status = extract_win_status(match_data['info']['participants'], puuid)
        if win_status is not None:
            save_win_status_to_file(directory_name, match_id, win_status)

        # Control the request rate to not exceed 50 requests per minute
        time.sleep(1.2)  # Sleep for 1.2 seconds between requests


if __name__ == "__main__":
    main()
