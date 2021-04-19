import json
import os
from warnings import warn

import measure
from utils.measurement import Measurement

# PUBLIC API
def calculate_RDTSC():
    warn("RDTSC baseline is not implemented. Using precomputed value.")
    RDTSC_baseline = 24.09245564 # TODO add actual benchmark code.
    _update_baselines_json(RDTSC_baseline=RDTSC_baseline)
    return RDTSC_baseline

def get_RDTSC(use_cached = True):
    if not use_cached:
        return calculate_RDTSC()
    else:
        try:
            with open("cache/baselines.json", 'r') as json_file:
                baseline_dict = json.load(json_file)
                return baseline_dict["RDTSC_baseline"]
        except FileNotFoundError as e:
            raise e("baselines.json not found. Run calculate_RDTSC function to create it.")
        except KeyError as e:
            raise e("The RDTSC overhead calculation has not been saved. Run calculate_RDTSC function to create it.")

def calculate_empty(python_path):
    measurement = measure.time_and_power(python_path, os.path.abspath("./baselines/empty.py"), iterations = 1000)
    _update_baselines_json(duration=measurement.duration, pkg=measurement.pkg, dram=measurement.dram)
    return measurement

def get_empty(python_path = None, use_cached = True):
    if not use_cached:
        if python_path is None:
            raise ValueError("If use_cached is False then python_path must be set.")
        return calculate_empty(python_path)
    else:
        try:
            with open("cache/baselines.json", 'r') as json_file:
                baseline_dict = json.load(json_file)
                return Measurement.from_dict(baseline_dict["empty_baseline"])
        except FileNotFoundError as e:
            raise e("baselines.json not found. Run calculate_empty function to create it.")
        except KeyError as e:
            raise e("The empty file overhead calculation has not been saved. Run calculate_empty function to create it.")

# PRIVATE
def _update_baselines_dict(baseline_dict, RDTSC_baseline = None, duration = None, pkg = None, dram = None):
    if RDTSC_baseline is not None:
        baseline_dict["RDTSC_baseline"] = RDTSC_baseline
    
    if duration is not None or pkg is not None and dram is not None:
        empty_dict = {}
        if duration is not None:
            empty_dict["duration"] = duration
        if pkg is not None:
            empty_dict["pkg"] = pkg
        if dram is not None:
            empty_dict["dram"] = dram
        baseline_dict["empty_baseline"] = empty_dict
    return baseline_dict

def _update_baselines_json(RDTSC_baseline = None, duration = None, pkg = None, dram = None):
    if(os.path.exists(os.path.abspath("./cache/baselines.json"))):
        with open("cache/baselines.json", 'r') as json_file:
            baseline_dict = json.load(json_file)
            baseline_dict = _update_baselines_dict(baseline_dict, RDTSC_baseline=RDTSC_baseline, duration=duration, pkg=pkg, dram=dram)
        with open("cache/baselines.json", 'w') as json_file:
            json.dump(baseline_dict, json_file)
            
    else:
        with open("cache/baselines.json", 'w') as json_file:
            baseline_dict = _update_baselines_dict({}, RDTSC_baseline=RDTSC_baseline, duration=duration, pkg=pkg, dram=dram)
            json.dump(baseline_dict, json_file)

