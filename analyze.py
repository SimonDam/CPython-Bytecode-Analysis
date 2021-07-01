import analysis.analysis as analysis
import argparse
import json
import multiprocessing as mp

import data.loader as loader
from Python.Lib.pathlib import Path
from data.csv_parser import csv_get_values
from analysis.visualise import create_graphs

def _get_count_and_sums_for_files_h(measurement, verbose):
    json_path = measurement.path_to_data.replace(".csv", ".json")
    csv_path = measurement.path_to_data
    res_dict = {}
    if verbose: print(f"Analyzing {csv_path}", flush=True)

    with open(csv_path) as file:
        for line in file:
            bytecode, value = csv_get_values(line)
            if bytecode == 'bytecode' and value == 'duration':
                continue # skip the header
            value = int(value)
            bytecode = int(bytecode)
            if bytecode in res_dict:
                res_dict[bytecode]['count'] += 1
                res_dict[bytecode]['sum'] += value
            else:
                # create the entry first time we encounter that bytecode
                res_dict[bytecode] = {'count': 1,'sum': value}
    _dump_cache(json_path, res_dict)
    return (measurement, res_dict)

def _load_existing_caches(measurement_lst):
    todo_lst = []
    done_lst = []
    
    for measurement, measurement_dict in measurement_lst:
        if "cache" in measurement_dict:
            done_lst.append((measurement, measurement_dict["cache"]))
        else:
            todo_lst.append(measurement)
    return todo_lst, done_lst

def get_count_and_sums_for_files(measurement_lst, verbose = False, nr_of_processes = 1, force = False):
    if nr_of_processes < 1:
        raise ValueError(f"nr_of_processes must be 1 or above ({nr_of_processes} given).")

    if not force:
        measurement_lst, bytecode_stat_lst = _load_existing_caches(measurement_lst)
        if measurement_lst == []:
            if verbose: print("Found caches for every .csv files. Set force flag not use caches.")
            return bytecode_stat_lst
        elif bytecode_stat_lst != []:
            if verbose: print("Found some caches. Set force flag not use caches.")

    args = []
    for measurement in measurement_lst:
        args.append((measurement, verbose))
    
    with mp.Pool(processes=nr_of_processes) as pool:
        results = pool.starmap(_get_count_and_sums_for_files_h, args)
    return bytecode_stat_lst + results

def _dump_cache(path, cache_dict):
    with open(Path(f"{path}"), 'r') as file:
        json_dict = json.load(file)
    json_dict["cache"] = cache_dict
    with open(Path(f"{path}"), 'w') as file:
        json.dump(json_dict, file, indent = 4)

if __name__ == "__main__":
    # Parse commandline args.
    parser = argparse.ArgumentParser()
    parser.add_argument("folder",
                        help="path to the directory of the .json files with paths to the .csv files.")
    parser.add_argument("-d", "--dest", default=None,
                        help="path to the results of the analysis/analyses.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print running statistics to the console.")
    parser.add_argument("-f", "--force", action="store_true", 
                        help="recalculate and override existing caches.")
    parser.add_argument("-p", "--processes", action="store", default=1, type=int,
                        help="amount of processes to run simultaniously. Useful for speeding up the calculation the cache statistics for each .csv file. Default is 1.")
    parser.add_argument("--train_split", action="store", default=1.0, type=float,
                        help="how much data should be used as training data. Should be > 0.0 and <= 1.0 Default is 1.0.")
    args = parser.parse_args()

    # Load data
    train, _, test = loader.read_from_folders(args.folder, samples_per_folder=(None, None, None), train_split = args.train_split, shuffle=True)
    train = get_count_and_sums_for_files(train, verbose = args.verbose, nr_of_processes = args.processes, force = args.force)
    test = get_count_and_sums_for_files(test, verbose = args.verbose, nr_of_processes = args.processes, force = args.force)

    sample_name = "All samples"

    # Get experiments
    analyses = []
    analyses += analysis.regression(sample_name)
    analyses += analysis.fraction_of_totals(sample_name)
    analyses += analysis.svm(sample_name)

    # Analyze data
    for a in analyses:
        data = a.run(train, test)
        create_graphs(data, a.name, dest = args.dest, show=args.verbose)
