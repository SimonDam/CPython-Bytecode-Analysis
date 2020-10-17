from pathlib import Path
import platform
import time
import sys
import argparse
import os
import json
import pyRAPL
import pandas as pd
from warnings import warn
from utils.printer import ow_print
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import jsonpickle
#from utils.setup import setup
class Bytecode_stat:
    __valid_bytecodes = {1,2,3,4,5,6,9,10,11,12,15,16,17,19,20,22,23,24,25,26,27,28,29,50,51,52,53,54,55,56,57,59,60,61,62,63,64,
                         65,66,67,68,69,70,71,72,73,75,76,77,78,79,81,82,83,84,85,86,87,88,89,90,90,91,92,93,94,95,96,97,98,100,101,
                         102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,122,124,125,126,130,131,132,133,135,136,137,138,
                         141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,160,161,162,163,257}
    def __init__(self, bytecode, timing, count = 1):
        if bytecode not in self.__valid_bytecodes:
            raise ValueError(f"{bytecode} is not a valid value for bytecode.")
        if timing < 0:
            raise ValueError(f"Timing can not be less than 0, {timing}.")
        if not isinstance(count, int):
            raise TypeError(f"count must be of type int, {type(count)} given.")
        if count < 1:
            raise ValueError(f"count must be 1 or higher, {count} given.")
        self.bytecode = bytecode
        self.timing = timing
        self.count = count
    
    def get_avg(self):
        return self.timing / self.count
    
    def __add__(self, other):
        if self.bytecode != other.bytecode:
            raise ValueError(f"Bytecodes must be the same, {self.bytecode} and {other.bytecode}.")
        return Bytecode_stat(self.bytecode, self.timing + other.timing, count = self.count + other.count)

    def __str__(self):
        return f"bytecode = {self.bytecode}, timing = {self.timing}, count = {self.count}"

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

def getPython_Paths():
    if(platform.platform().startswith("Windows")):
        return os.path.abspath("./Python/python.bat"), os.path.abspath("./Python-BCT/Python.bat")
    else:
        return os.path.abspath("./Python/python"), os.path.abspath("./Python-BCT/python")

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

def ensure_BCT_dir(BCT_path):
    while True:
        if not os.path.isdir(BCT_path):
            answer = input("The directory specified in bcc.txt does not exist. Do you want to create it? (Y/N)").upper()
            if answer in ("Y", "YES"):
                try:
                    os.makedirs(BCT_path)
                except OSError as error:
                    print(f"Unable to create directory at {BCT_path}. {error}")
                else:
                    return BCT_path
        else:
            return BCT_path
        BCT_path = input("Please specify a folder to write bytecodes to: ")

def get_BCT_path():
    os.chdir(os.path.abspath("./Python-BCT"))
    BCT_path = ""
    if os.path.isfile("bcc.txt"):
        with open("bcc.txt", 'r') as bct_file:
            BCT_path =  bct_file.readline()
            BCT_path = ensure_BCT_dir(BCT_path)
    else:
        with open("bcc.txt", 'w') as bct_file:
            BCT_path = ensure_BCT_dir("")
            bct_file.write(BCT_path)
    os.chdir(os.path.abspath(".."))
    return BCT_path

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

def ensure_compilied():
    # TODO implement this
    warn("ensure_compiled is not implemented.")

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir",
                        help="path to the directory of the .py-files to be run.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print running statistics to the console.")
    parser.add_argument("-f", "--force", action="store_true", 
                        help="measure all programs regardless if they have already been measured.")
    return parser.parse_args()

def measure_program(filepath, vanilla_path, bc_path, iterations = 1, verbose = False, time_limit = float('+inf')):
    # Measure time and energy consumption
    measurement = get_time_and_power(vanilla_path, filepath, iterations = iterations, verbose = verbose, time_limit=time_limit)
    # Time bytecodes
    run_BCTs(bc_path, filepath, verbose = verbose)
    return measurement

def setup():
    pyRAPL.setup()
    ensure_compilied()
    vanilla_path, bc_path = getPython_Paths()
    BCT_path = get_BCT_path()
    
    # We handle the case there the user did or did not add the path seperator to their input.
    args = get_args()
    if not args.source_dir.endswith(os.sep):
        args.source_dir += os.sep
    return vanilla_path, bc_path, args, BCT_path

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

def compute_bc_stats(csv_path):
    bytecode_dict = {}
    for chunk in pd.read_csv(csv_path, chunksize = 1000000):
        for index, bytecode, timing in chunk.itertuples():
            bytecode_stat = Bytecode_stat(bytecode, timing)
            if bytecode in bytecode_dict:
                bytecode_dict[bytecode] += bytecode_stat
            else:
                bytecode_dict[bytecode] = bytecode_stat
    return bytecode_dict

def read_meta_json_as_dict(json_path):
    with open(json_path, 'r') as BCT_file:
        results_dict = json.load(BCT_file)

    if 'bc_stats' in results_dict:
        bc_stats = {}
        for key in results_dict['bc_stats']:
            bc_stats[key] = jsonpickle.decode(results_dict['bc_stats'][key])
        results_dict['bc_stats'] = bc_stats

    return results_dict

def write_meta_dict_as_json(results_dict, json_path):
    bc_stats = {}
    results_copy = results_dict.copy()
    for key in results_copy['bc_stats']:
        bc_stats[key] = jsonpickle.encode(results_copy['bc_stats'][key])

    results_copy['bc_stats'] = bc_stats

    with open(json_path, 'w') as json_file:
        json.dump(results_copy, json_file)

def main():
    vanilla_path, bc_path, args, BCT_path = setup()
    "/home/simon/Desktop/testfolder"

    measurement_lst = []
    results_lst  = []

    for filename in os.listdir(args.source_dir):
        if filename.endswith(".py"):
            filepath = f"{args.source_dir}{filename}"
            json_path = f"{BCT_path}{filename}.json"
        
            if args.force or not file_already_run(json_path):
                measurement = measure_program(filepath, vanilla_path, bc_path, iterations = 100, verbose = args.verbose, time_limit=10)
                measurement_lst += [measurement]
                
                results_dict = read_meta_json_as_dict(json_path)
                results_dict['duration'] = measurement.duration
                results_dict['pkg'] = measurement.pkg
                results_dict['dram'] = measurement.dram
                results_dict['is_measured'] = True
                results_dict['bc_stats'] = compute_bc_stats(results_dict['bct_path'])
                
                write_meta_dict_as_json(results_dict, json_path)

            else:
                if args.verbose:
                    print(f"Skipping {filename} (already measured). See --help to override this.")
                results_dict = read_meta_json_as_dict(json_path)

            measurement_lst.append(Measurement(results_dict['duration'], results_dict['pkg'], results_dict['dram'], name = filename))
            results_lst.append(results_dict)

    duration_lst = [x.duration for x in measurement_lst]
    pkg_lst = [sum(x.pkg) for x in measurement_lst]
    dram_lst = [sum(x.dram) for x in measurement_lst]
    
    pkg_fig, pkg_ax = plt.subplots()
    pkg_ax.set_title("Run-time vs. CPU energy consumption.")
    pkg_ax.set_xlabel("Time [µs]")
    pkg_ax.set_ylabel("Energy [µJ]")
    pkg_ax.scatter(duration_lst, pkg_lst)
    pkg_fig.savefig(f"{BCT_path}cpu.pdf")
    pkg_fig.show()

    dram_fig, dram_ax = plt.subplots()
    dram_ax.set_title("Run-time vs. RAM energy consumption.")
    dram_ax.set_xlabel("Time [µs]")
    dram_ax.set_ylabel("Energy [µJ]")
    dram_ax.scatter(duration_lst, dram_lst)
    dram_fig.savefig(f"{BCT_path}ram.pdf")
    dram_fig.show()

    sum_results = {}
    for results in results_lst:
        for key in results['bc_stats']:
            if key in sum_results:
                sum_results[key] += results['bc_stats'][key]
            else:
                sum_results[key] = results['bc_stats'][key]

    # Calculate duration from the average timing of a bytecode, multiplied by the amount of times it has been seen.
    #duration_lst = []
    #for results in results_lst:
    #    duration = 0
    #    for key in results['bc_stats']:
    #        avg = sum_results[key].get_avg()
    #        count = results['bc_stats'][key].count
    #        duration +=  avg * count
    #    duration_lst.append((results['bct_path'], duration, results['duration'], duration / results['duration']))

    sum_dur = 0
    for key in sum_results:
        sum_dur += sum_results[key].timing

    percentage_dict = {}
    for key in sum_results:
        percentage_dict[key] = sum_results[key].timing / sum_dur

    #TODO Calculate the average energy consumption of each bytecode based on the amount of time it takes to execute it, compared to the total time.
    #     Use this to calculate the total energy consumption by simply multiplying the energy consumption of each bytecode with the amount of times it has been executed.

if __name__ == "__main__":
    main()
