import argparse
import os
import platform
from warnings import warn

import pyRAPL


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

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir",
                        help="path to the directory of the .py-files to be run.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print running statistics to the console.")
    parser.add_argument("-f", "--force", action="store_true", 
                        help="measure all programs regardless if they have already been measured.")
    return parser.parse_args()

def _ensure_compiled():
    # TODO implement this
    warn("_ensure_compiled is not implemented.")

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

def getPython_Paths():
    if(platform.platform().startswith("Windows")):
        return os.path.abspath("./Python/python.bat"), os.path.abspath("./Python-BCT/Python.bat")
    else:
        return os.path.abspath("./Python/python"), os.path.abspath("./Python-BCT/python")

def setup():
    pyRAPL.setup()
    vanilla_path, bc_path = getPython_Paths()
    _ensure_compiled()
    BCT_path = get_BCT_path()
    
    # We handle the case there the user did or did not add the path seperator to their input.
    args = get_args()
    if not args.source_dir.endswith(os.sep):
        args.source_dir += os.sep
    return vanilla_path, bc_path, args, BCT_path
