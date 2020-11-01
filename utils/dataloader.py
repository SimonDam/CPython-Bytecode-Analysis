from pathlib import Path
import os
import json
import pandas as pd
from utils.measurement import Measurement

def read_jsons(path):
    measurement_lst = []
    for filename in os.listdir(path):
        if filename.endswith(".json"):
            with open(Path(f"{path}/{filename}")) as file:
                data_dict = json.load(file)
                print(data_dict, filename)
                duration = data_dict["duration"]
                pkg = data_dict["pkg"]
                dram = data_dict["dram"]
                path_to_data = data_dict["bct_path"]
                measurement = Measurement(duration, pkg, dram, path_to_data = path_to_data)
                measurement_lst.append(measurement)
    return measurement_lst
