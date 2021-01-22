from utils.measurement import Measurement
from measure import get_time_and_power
import os
from warnings import warn
import json

def RDTSC_baseline():
    # TODO add actual benchmark code.
    warn("RDTSC baseline is not implemented. Using precomputed value.")
    return 24.143901008216858

def empty_program_baseline(python_path, force=True, iterations=10000):
    measurement = None
    file_exists = os.path.exists(os.path.abspath("./cache/baselines.json"))
    get_baseline_measurement = lambda: get_time_and_power(python_path, os.path.abspath("./baselines/empty.py"), iterations=iterations)

    if force or not file_exists:
        measurement = get_baseline_measurement()

    if file_exists:
        with open(os.path.abspath("./cache/baselines.json", 'r')) as json_file:
            baseline_dict = json.load(json_file)
            measurement = Measurement(baseline_dict["duration"], baseline_dict["pkg"], baseline_dict["dram"])
    else:
        with open(os.path.abspath("./cache/baselines.json", 'w')) as json_file:
            baseline_dict = {
                "empty_baseline": {
                    "duration": measurement.duration,
                    "pkg": measurement.pkg,
                    "dram": measurement.dram
                },
                "RDTSC_basline":"Null"
            }
            baseline_dict["duration"] = measurement.duration
            baseline_dict["pkg"] = measurement.duration
            baseline_dict["dram"] = measurement.duration
            json.dump(baseline_dict, json_file)
    return measurement
    
