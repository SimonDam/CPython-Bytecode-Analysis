import os
import sys
import time
from pathlib import Path
import tempfile
import argparse
import inspect
import subprocess
import json

def import_module_by_path(path):
    name = os.path.splitext(os.path.basename(path))[0]
    if sys.version_info[0] == 2:
        import imp
        return imp.load_source(name, path)
    elif sys.version_info[:2] <= (3, 4):
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader(name, path).load_module()
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

def _verify_args(target, timeout, error):
    if type(target) not in (float, int):
        raise TypeError(f"type(target)={type(target)} has to be either float or int.")
    if target <= 0:
        raise ValueError(f"target={target} must larger than 0.")


    if type(error) not in (float, int):
        raise TypeError(f"type(error)={type(error)} has to be either float or int.")
    if not (0 < error < 1):
        raise ValueError(f"error={error} must between 0 and 1.")

    if timeout is not None:
        if type(timeout) not in (float, int):
            raise TypeError(f"type(timeout)={type(timeout)} has to be either float or int.")
        if timeout <= 0:
            raise ValueError(f"timeout={timeout} must larger than 0.")
        if timeout < target:
            raise ValueError(f"target={target} must be smaller than timeout={timeout}.")

def _change(elapsed, change, min, max, prev):
    if min < elapsed < max:
        return 0, ""

    if elapsed < min:
        if prev == "above":
            change = abs(change // 2)
        else:
            change *= 2
        prev = "below"

    elif elapsed > max:
        if prev == "below":
            change = -(change // 2)
        else:
            change //= 2
        prev = "above"
    return change, prev

def _temp_folder_cleanup(folder, max_attempts = 1000):
    delete_fail_count = 0
    while len(os.listdir(folder)) != 0 and delete_fail_count <= max_attempts:
        for file in os.listdir(folder):
            try:
                # The process might still have control over the file.
                os.remove(Path(f"./{folder}/{file}"))
            except:
                delete_fail_count += 1
    if delete_fail_count > max_attempts:
        print(f"Unable to clean up temp folder, located at: {folder}. Probably because another process is using some of the files in that folder.")

def find_min(source_code_func, timeout):
    n = 1
    succeed = False
    while not succeed:
        source_str = source_code_func(n)

        with tempfile.NamedTemporaryFile(dir = Path("./temp"), mode = 'w', delete=False, encoding="utf8") as file:
            filepath = file.name
            file.write(source_str)

        try:
            process = subprocess.run([sys.executable, filepath], timeout=timeout)
        except:
            n += 1
        else:
            if process.returncode == 0:
                succeed = True
            else:
                n += 1
    _temp_folder_cleanup("./temp")
    return n

def find_max(source_code_func, timeout, target_min, target_max, min_n):
    valid_n = None
    n = min_n
    change = 1
    prev = "below"
    while change != 0:
        print(n, end = " ", flush=True)
        source_str = source_code_func(n)

        filepath = ""
        with tempfile.NamedTemporaryFile(dir = Path("./temp"), mode = 'w', delete=False, encoding="utf8") as file:
            filepath = file.name
            file.write(source_str)

        try:
            start = time.time()
            process = subprocess.run([sys.executable, filepath], timeout=timeout)
            elapsed = time.time()-start
        except subprocess.TimeoutExpired:
            elapsed = float("+inf")
        except MemoryError:
            elapsed = float("+inf")
        else:
            # The case where the program fails. We assume the n is too small.
            if process.returncode == 0:
                valid_n = n
            else:
                # TODO, this is a problem for programs, where large n's result in failure.
                # In this case, case it continues to increase n, despite it keeps failing.
                elapsed = float("-inf")

        change, prev = _change(elapsed, change, target_min, target_max, prev)
        n += change
        if n < 1:
            n = 1
        if n > 2**1000:
            # TODO Temporary solution for the case where the programs is too large.
            return None
    return valid_n

def generate_min_max(folder, target, timeout=None, error = 0.05):
    _verify_args(target, timeout, error)
    if timeout is None:
        timeout = (target * 2) + 1

    target_min = target * (1 - error)
    target_max = target * (1 + error)

    temp_folder = Path("./temp")
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    
    json_path = Path(f"{folder}/timing_statistics.json")
    if not os.path.exists(json_path):
        with open(json_path, 'w') as json_file:
            json_dict = {}
            json_file.write("")
    else:
        with open(json_path, 'r') as json_file:
            json_dict = json.load(json_file)

    for program in os.listdir(folder):
        if program.endswith(".py"):
            print(f"Finding n for: {program}... ", end= "", flush=True)
            program_path = Path(f"{folder}/{program}")
            module = import_module_by_path(program_path)
            source_code_func = module.source_code

            num_of_params = len(inspect.getfullargspec(source_code_func).args)
            if num_of_params == 0:
                # In this case, there is nothing to benchmark, therefore we just skip this file.
                continue
            if num_of_params > 1:
                raise TypeError(f"source_code_func must only take 0 or 1 inputs, but is defined with {num_of_params} parameters. Consider reading fixer.py for more.")
            
            min_n = find_min(source_code_func, timeout)
            n = find_max(source_code_func, timeout, target_min, target_max, min_n)

            stats_dict = {
                        "n": n,
                        "min_n": min_n,
                        "target_time":target,
                        "timeout":timeout
                    }

            if program in json_dict:
                json_dict[program] = json_dict[program].append(stats_dict)
            else:
                json_dict[program] = {[stats_dict]}
            
            with open(json_path, 'w') as json_file:
                json.dump(json_dict, json_file)
            
            print(f"Found {n} and min {min_n}", flush=True)
        _temp_folder_cleanup(temp_folder)
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir",
                        help="path to the directory of the .py-files to be run.")
    parser.add_argument("target", type=float,
                        help="Target run-time in seconds for the program.")
    parser.add_argument("--timeout", type=float,
                        help="the maximum run-time in seconds before timing out the program.")
    parser.add_argument("--error", type=float, default=0.05,
                        help=f"the error from the target run-time that is considered acceptable. Default is 0.05.")
    
    args = parser.parse_args()
    
    generate_min_max(args.source_dir, args.target, timeout=args.timeout, error=args.error)