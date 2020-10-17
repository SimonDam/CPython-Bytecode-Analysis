import os
import pyRAPL
import time
from utils.printer import ow_print
import json

class Measurement:
    def __init__(self, duration, pkg, dram, name = None):
        if duration < 0:
            raise ValueError(f"Duration must be positive. {duration}")
        for cpu_energy in pkg:
            if cpu_energy < 0:
                raise ValueError(f"All elements of pkg must be positive. {pkg}")
        for ram_energy in dram:
            if ram_energy < 0:
                raise ValueError(f"All elements of pkg must be positive. {dram}")
        if name is not None:
            if not isinstance(name, str):
                raise TypeError(f"name must be of type string.")
        
        self.duration = duration
        self.pkg = pkg
        self.dram = dram
        self.name = name

    def __add__(self, other):
        name = None
        if self.name is not None: 
            name = self.name
        if other.name is not None:
            name = other.name

        self.__validate_other(other)
        duration = self.duration + other.duration
        pkg = [x + y for x, y in zip(self.pkg, other.pkg)]
        dram = [x + y for x, y in zip(self.dram, other.dram)]
        return Measurement(duration, pkg, dram, name)

    def __truediv__(self, dividend):
        duration = self.duration / dividend
        pkg = [x / dividend for x in self.pkg]
        dram = [x / dividend for x in self.dram]
        return Measurement(duration, pkg, dram, self.name)

    def __validate_other(self, other):
        if len(self.pkg) != len(other.pkg):
            raise ValueError(f"pkg lists must be same length.")
        if len(self.dram) != len(other.dram):
            raise ValueError(f"dram lists must be same length.")

    def __str__(self):
        if self.name is not None:
            return f"Name: {self.name} Duration: {self.duration} pkg: {self.pkg} dram: {self.dram}"
        else:
            return f"Duration: {self.duration} pkg: {self.pkg} dram: {self.dram}"

def run_BCTs(python_path, filepath, verbose = False):
    if verbose:
        filename = filepath.split(os.sep)[-1]
        print(f"Timing bytecodes of {filename}...", end = ' ', flush = True)
    os.chdir(os.path.abspath("./Python-BCT"))
    # Run the modified Python interpreter.
    os.system(f"{python_path} {filepath}")
    # This has generated the bytecode files.
    os.chdir(os.path.abspath(".."))
    if verbose:
        print("Done!")

def get_time_and_power(python_path, filepath, iterations = 1, time_limit = float('+inf'), verbose = False):
    name = filepath.split(os.sep)[-1]
    pyRAPL_measurement = pyRAPL.Measurement(name)
    measurement = Measurement(0.0, [0.0], [0.0], name = name) # TODO edit to accomodate variable length pkg/dram
    dividend = 0
    start = time.time()
    for i in range(iterations):
        dividend = i + 1
        pyRAPL_measurement.begin()
        os.system(f"{python_path} {filepath}")
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
    measurement = get_time_and_power(vanilla_path, filepath, iterations = iterations, verbose = verbose, time_limit=time_limit)
    # Time bytecodes
    run_BCTs(bc_path, filepath, verbose = verbose)
    return measurement

def file_already_run(json_path):
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

def measure_programs(programs_dir, vanilla_path, bc_path, BCT_path, force = False, verbose = False):
    measurement_lst = []

    for filename in os.listdir(programs_dir):
        if filename.endswith(".py"):
            filepath = f"{programs_dir}{filename}"
            json_path = f"{BCT_path}{filename}.json"
        
            if force or not file_already_run(json_path):
                measurement = measure_program(filepath, vanilla_path, bc_path, iterations = 100, verbose = verbose, time_limit=10)
                measurement_lst.append(measurement)
                with open(json_path, 'r') as BCT_file:
                    results_dict = json.load(BCT_file)
                    results_dict['duration'] = measurement.duration
                    results_dict['pkg'] = measurement.pkg
                    results_dict['dram'] = measurement.dram
                    results_dict['is_measured'] = True
                with open(json_path, 'w') as json_file:
                    json.dump(results_dict, json_file)


            else:
                if verbose:
                    print(f"Skipping {filename} (already measured). See --help to override this.")
                with open(json_path, 'r') as BCT_file:
                    results_dict = json.load(BCT_file)

            measurement_lst.append(Measurement(results_dict['duration'], results_dict['pkg'], results_dict['dram'], name = filename))
    return measurement_lst