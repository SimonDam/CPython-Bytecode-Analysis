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

def main():
    vanilla_path, bc_path, args, BCT_path = setup()
    "/home/simon/Desktop/testfolder"

    duration_lst = []
    pkg_lst = []
    dram_lst = []


    for filename in os.listdir(args.source_dir):
        if filename.endswith(".py"):
            do_run = False
            filepath = f"{args.source_dir}{filename}"
            json_path = f"{BCT_path}{filename}.json"
            
            if args.force:
                do_run = True
            elif not os.path.isfile(json_path):
                do_run = True
            else:
                with open(json_path) as json_file:
                    try: # In case of invalid json.
                        metadata_dict = json.load(json_file)
                    except:
                        do_run = True
                    else:
                        if 'is_measured' not in metadata_dict and not metadata_dict['is_measured']:
                            do_run = True

            if do_run:
                measurement = measure_program(filepath, vanilla_path, bc_path, iterations = 100, verbose = args.verbose, time_limit=10)
                with open(json_path, 'r') as BCT_file:
                    metadata_dict = json.load(BCT_file)
                BCT_pd = pd.read_csv(metadata_dict['bct_path'])
                metadata_dict['duration'] = measurement.duration
                duration_lst += [metadata_dict['duration']]

                metadata_dict['pkg'] = measurement.pkg
                pkg_lst += [sum(metadata_dict['pkg'])]
                

                metadata_dict['dram'] = measurement.dram
                dram_lst += [sum(metadata_dict['dram'])]

                metadata_dict['is_measured'] = True

                with open(json_path, 'w') as json_file:
                    json.dump(metadata_dict, json_file)
            elif args.verbose:
                print(f"Skipping {filename} (already measured). See --help to override this.")
    
    
    #pkg_fig, pkg_ax = plt.subplots() 
    #dram_fig, dram_ax = plt.subplots()
    #pkg_ax.scatter(duration_lst, pkg_lst)
    #dram_ax.scatter(duration_lst, dram_lst)
    #pkg_fig.show()
    #input()
    #dram_fig.show()
    #input()

if __name__ == "__main__":
    main()
