from pathlib import Path
import platform
import time
import sys
import os
import json
import pyRAPL
import pandas as pd
from warnings import warn
from utils.printer import ow_print
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from utils.setup import setup
from measure import measure_programs, Measurement

def main():
    vanilla_path, bc_path, args, BCT_path = setup()
    measurement_lst = measure_programs(args.source_dir, vanilla_path, bc_path, BCT_path, force = args.force, verbose = args.verbose)

if __name__ == "__main__":
    main()
