import json
import sys
import os
from pathlib import Path

def update_paths(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            json_filename = filename.split('.csv')[0] + ".json"
            json_path = Path(f"{folder}/{json_filename}")

            with open(json_path, 'r') as json_file:
                json_dict = json.load(json_file)

            json_dict['bct_path'] = os.path.join(folder, filename)
            with open(json_path, 'w') as json_file:
                json.dump(json_dict, json_file, indent = 4)

def main():
    folder = sys.argv[1]
    update_paths(folder)


if __name__ == "__main__":
    main()