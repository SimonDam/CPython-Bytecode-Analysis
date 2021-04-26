import os
import pyRAPL
import time
from utils.printer import ow_print
import json
from utils.measurement import Measurement
from pathlib import Path

def run_BCTs(python_path, filepath, verbose = False):
    if verbose:
        filename = filepath.split(os.sep)[-1]
        print(f"Timing bytecodes of {filename}...", end = ' ', flush = True)
    os.chdir(os.path.abspath("./Python-BCT")) # TODO Avoid changing directory.
    # Run the modified Python interpreter.
    os.system(f"{python_path} {filepath}") # TODO Add CPU affinity for this benchmark.
    # This has generated the bytecode files.
    os.chdir(os.path.abspath(".."))
    if verbose:
        print("Done!")

def time_and_power(python_path, filepath, iterations = 1, time_limit = float('+inf'), verbose = False):
    # ensure that filepath is a Path object
    filepath = Path(filepath)
    name = filepath.name

    pyRAPL_measurement = pyRAPL.Measurement(name)
    measurement = Measurement(0.0, [0.0], [0.0], name = name) # TODO edit to accomodate variable length pkg/dram
    dividend = 0
    start = time.time()
    for i in range(iterations):
        dividend = i + 1
        pyRAPL_measurement.begin()
        os.system(f"{python_path} {filepath}") # TODO Add CPU affinity for this benchmark.
        pyRAPL_measurement.end()
        measurement += Measurement(pyRAPL_measurement.result.duration,
                                   pyRAPL_measurement.result.pkg,
                                   pyRAPL_measurement.result.dram, 
                                   name = name)
        if verbose:
            ow_print(f"Iteration {dividend}/{iterations} of {name}: {measurement / dividend}")
        if time.time() - start > time_limit:
            if verbose:
                print()
                print(f"Breaking at iteration {dividend}/{iterations} due to exceeding time limit.")
            break
    if verbose:
        print()
    return measurement / dividend

def measure_program(filepath, vanilla_path, bc_path, iterations = 1, verbose = False, time_limit = float('+inf')):
    # Measure time and energy consumption
    measurement = time_and_power(vanilla_path, filepath, iterations = iterations, verbose = verbose, time_limit=time_limit)
    # Time bytecodes
    run_BCTs(bc_path, filepath, verbose = verbose)
    return measurement

def _file_already_run(json_path):
    try: # Catch if file does not exist, or if the json is invalid.
        with open(json_path) as json_file:
            metadata_dict = json.load(json_file)
    except: # We don't care which error is it, we just rerun.
        return False
    else:
        if 'is_measured' not in metadata_dict:
            return False
        elif not metadata_dict['is_measured']:
            return False
        else:
            return True

def measure_programs(programs_dir, vanilla_path, bc_path, BCT_path, force = False, iterations = 1, time_limit = float("+inf"), verbose = False):
    for filename in os.listdir(programs_dir):
        if filename.endswith(".py"):
            filepath = Path(f"{programs_dir}/{filename}")
            json_path = Path(f"{BCT_path}/{filename}.json")
        
            if force or not _file_already_run(json_path):
                measurement = measure_program(filepath, vanilla_path, bc_path, iterations = iterations, verbose = verbose, time_limit=time_limit)
                with open(json_path, 'r') as BCT_file:
                    results_dict = json.load(BCT_file)
                    results_dict.update(measurement.as_dict())
                    results_dict['is_measured'] = True
                with open(json_path, 'w') as json_file:
                    json.dump(results_dict, json_file)
            else:
                if verbose:
                    print(f"Skipping {filename} (already measured). See --help to override this.")
