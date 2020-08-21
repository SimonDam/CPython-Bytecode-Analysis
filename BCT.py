from pathlib import Path
import platform
import time
import os
import json
import pyRAPL

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

def measure_program(python_path, filepath, iterations = 1, max_dur = float('+inf')):
    name = filepath.split('/')[-1]
    pyRAPL_measurement = pyRAPL.Measurement("name")
    measurement = Measurement(0.0, [0.0], [0.0], name = name)
    dividend = 1
    start = time.time()
    for i in range(iterations):
        dividend += 1
        pyRAPL_measurement.begin()
        os.system(f"{python_path} {filepath}")
        pyRAPL_measurement.end()
        measurement += Measurement(pyRAPL_measurement.result.duration,
                                   pyRAPL_measurement.result.pkg,
                                   pyRAPL_measurement.result.dram, 
                                   name = name)
        if time.time() - start > max_dur:
            break
    
    return measurement / dividend

def get_BCTs(python_path, filepath):
    os.chdir(os.path.abspath("./Python-BCT"))
    os.system(f"{python_path} {filepath}")
    with open(Path(f"bcc.txt")) as bcc_file:
        BCT_path =  bcc_file.readline()

    filename = filepath.split(os.sep)[-1]
    with open(f"{BCT_path}{filename}.json", 'r') as BCT_file:
        json_str = BCT_file.readline()
    os.chdir(os.path.abspath(".."))
    return json.loads(json_str)

def main():
    pyRAPL.setup()

    vanilla_path, bc_path = getPython_Paths()
    filepath = "/home/simon/Desktop/empty.py"
    measurement = measure_program(str(vanilla_path), filepath, iterations = 10)
    BCT_json = get_BCTs(str(bc_path), filepath)


if __name__ == "__main__":
    main()
