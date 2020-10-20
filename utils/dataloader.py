from pathlib import Path
import os
import json
import pandas as pd

def read_jsons(path):
    json_lst = []
    for filename in os.listdir(path):
        if filename.endswith(".json"):
            with open(Path(f"{path}/{filename}")) as file:
                json_lst.append(json.load(file))
    return json_lst
