import os
import json

def extract_info(participant):
    return {
        "ennemyMissingPings": participant.get("enemyMissingPings", 0),
        "win": participant.get("win", False),
        "championName": participant.get("championName", ""),
        "kda": participant.get("challenges", {}).get("kda", 0.0),
        "position": participant.get("individualPosition", ""),
        "pentakills": participant.get("missions", {}).get("pentakills", 0),
        "totalMinionsKilled": participant.get("totalMinionsKilled", 0),
        "turretsLost": participant.get("turretsLost", 0)
    }

def process_files(input_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            input_filepath = os.path.join(input_folder, filename)
            with open(input_filepath) as f:
                data = json.load(f)

            participants = data.get("info", {}).get("participants", [])
            output_folder = f"{input_folder}_onelined_parsed"
            os.makedirs(output_folder, exist_ok=True)

            for index, participant in enumerate(participants):
                extracted_data = extract_info(participant)
                output_filename = f"{os.path.splitext(filename)[0]}_onelined_parsed_{index+1}.json"
                output_filepath = os.path.join(output_folder, output_filename)
                with open(output_filepath, 'w') as outfile:
                    json.dump(extracted_data, outfile, separators=(',', ':'))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process JSON files in a folder.")
    parser.add_argument("input_folder", type=str, help="Relative path to the input folder containing JSON files.")
    
    args = parser.parse_args()
    process_files(args.input_folder)
