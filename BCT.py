from pathlib import Path
import platform
import time
import os
import json
import pyRAPL
import pandas as pd

class BC_timing:
    def __init__(self, opcode, timing, f):
        pass

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

def measure_program(python_path, filepath, iterations = 1, max_dur = float('+inf'), verbose = False):
    name = filepath.split(os.sep)[-1]
    pyRAPL_measurement = pyRAPL.Measurement("name")
    measurement = Measurement(0.0, [0.0], [0.0], name = name)
    dividend = 0
    start = time.time()
    for i in range(iterations):
        dividend += 1
        if verbose:
            print(f"Running iteration {dividend} of {name}... ", end='')
        pyRAPL_measurement.begin()
        os.system(f"{python_path} {filepath}")
        pyRAPL_measurement.end()
        measurement += Measurement(pyRAPL_measurement.result.duration,
                                   pyRAPL_measurement.result.pkg,
                                   pyRAPL_measurement.result.dram, 
                                   name = name)
        if verbose:
            print(measurement / dividend)
        if time.time() - start > max_dur:
            if verbose:
                print(f"Breaking at iteration {dividend} due to exceeding time limit.")
            break
    
    return measurement / dividend

def validate_BCT_dir(BCT_path):
    while True:
        if not os.path.isdir(BCT_path):
            answer = input("The directory specified in bcc.txt does not exist. Do you want to create it? (Y/N)").upper()
            if answer in ("Y", "YES"):
                try:
                    os.makedirs(BCT_path)
                except OSError:
                    print(f"Creation of directory at {BCT_path} failed.")
                else:
                    return BCT_path
        else:
            return BCT_path
        BCT_path = input("Please specify a folder to write bytecodes to: ")

def get_BCT_path():
    os.chdir(os.path.abspath("./Python-BCT"))
    BCT_path = ""
    if os.path.isfile("bcc.txt"):
        with open("bcc.txt", 'r') as bcc_file:
            BCT_path =  bcc_file.readline()
            BCT_path = validate_BCT_dir(BCT_path)
    else:
        with open("bcc.txt", 'w') as bcc_file:
            BCT_path = validate_BCT_dir(BCT_path)
            bcc_file.write(BCT_path)
    os.chdir(os.path.abspath(".."))
    return BCT_path

def get_BCTs(python_path, filepath):
    os.chdir(os.path.abspath("./Python-BCT"))
    # Run the modified Python interpreter.
    os.system(f"{python_path} {filepath}")
    # This has generated the bytecode files.
    os.chdir(os.path.abspath(".."))
    
    # We need to get that path here.
    BCT_path = get_BCT_path()

    filename = filepath.split(os.sep)[-1]
    with open(f"{BCT_path}{filename}.json", 'r') as BCT_file:
        meta_data = json.load(BCT_file)

    return pd.read_csv(meta_data['bct_path'])

def main():
    pyRAPL.setup()

    vanilla_path, bc_path = getPython_Paths()
    filepath = "/home/simon/Desktop/forloop.py"
    measurement = measure_program(vanilla_path, filepath, iterations = 100, verbose = True, max_dur=10)
    
    BCT_pd = get_BCTs(bc_path, filepath)
    #print(BCT_pd)


if __name__ == "__main__":
    main()
