from pathlib import Path
import platform
import time
import os
import json
import pyRAPL

class BC_timing:
    def __init__(self, opcode, timing, f):
        pass

def getPython_Paths():
    if(platform.platform().startswith("Windows")):
        vanilla_path = Path("./Python/python.bat")
        bc_path = Path("./Python-BCT/Python.bat")
    else:
        vanilla_path = Path("./Python/python")
        bc_path = Path("./Python-BCT/python")
    
    return vanilla_path, bc_path

def time_Python_program(python_path, filepath):
    start = time.time()
    os.system(f"{python_path} {filepath}")
    return time.time() - start

def get_BCTs(python_path, filepath):
    os.system(f"{python_path} {filepath}")
    with open(Path(f"./Python-BCT/bcc.txt")) as bcc_file:
        BCT_path =  bcc_file.readline()

    filename = filepath.split(os.sep)[-1]
    with open(f"{BCT_path}{filename}.BCT", 'r') as BCT_file:
        json_str = BCT_file.readline()

    return json.loads(json_str)


def main():
    vanilla_path, bc_path = getPython_Paths()
    filepath = "/home/simon/Desktop/empty.py"
    time = time_Python_program(str(vanilla_path), filepath)
    BCT_json = get_BCTs(str(filepath), filepath)


if __name__ == "__main__":
    main()
