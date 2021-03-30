import argparse
import json
import multiprocessing as mp
import os
import sys

from numpy.lib.function_base import average

import utils.dataloader as dataloader
import data.processing as processing
import data.preparation as preparation
from Python.Lib.pathlib import Path
from utils.csv_parser import csv_get_values

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def get_count_and_sums_for_files_h(measurement, verbose):
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
    dump_cache(json_path, res_dict)
    return (measurement, res_dict)

def load_existing_caches(measurement_lst):
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
        measurement_lst, bytecode_stat_lst = load_existing_caches(measurement_lst)
        if measurement_lst == []:
            if verbose: print("Found caches for every .csv files. Set force flag not use caches.")
            return bytecode_stat_lst
        elif bytecode_stat_lst != []:
            if verbose: print("Found some caches. Set force flag not use caches.")

    args = []
    for measurement in measurement_lst:
        args.append((measurement, verbose))
    
    with mp.Pool(processes=nr_of_processes) as pool:
        results = pool.starmap(get_count_and_sums_for_files_h, args)
    return bytecode_stat_lst + results

def dump_cache(path, cache_dict):
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
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print running statistics to the console.")
    parser.add_argument("-f", "--force", action="store_true", 
                        help="recalculate and override existing caches.")
    parser.add_argument("-p", "--processes", action="store", default=1, type=int,
                        help="amount of processes to run simultaniously. Useful for speeding up the calculation the cache statistics for each .csv file. Default is 1.")
    args = parser.parse_args()

    # Load data
    train, _, test = dataloader.read_from_folders(args.folder, train_split=0.7, samples_per_folder=(None, None, None), shuffle=True)
    train = get_count_and_sums_for_files(train, verbose = args.verbose, nr_of_processes = args.processes, force = args.force)
    test = get_count_and_sums_for_files(test, verbose = args.verbose, nr_of_processes = args.processes, force = args.force)

    # Analyze data
    result_lst = processing.fraction_of_totals.get_results(train, test)
    #result_lst = processing.regression.get_results(train, test, use_baseline = False)
    xs = []
    ys = []
    errors = []
    with open("regression.csv", 'w') as file:
        file.write("path,estimated_energy,actual_energy\n")
        for path, estimated_energy, actual_energy in result_lst:
            xs.append(actual_energy)
            ys.append(estimated_energy)
            error = abs(actual_energy-estimated_energy)/actual_energy
            errors.append(error*100)
            file.write(f"\"{path}\",{estimated_energy},{actual_energy}\n")
    
    avg_error = average(errors)
    print("Score", avg_error)
    correlation_matrix = np.corrcoef(xs, ys)
    correlation_xy = correlation_matrix[0,1]
    r_squared = correlation_xy ** 2
    print("R^2", r_squared)
    
    # Fit a linear line to data.
    z = np.polyfit(xs, ys, 1)
    p = np.poly1d(z)
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,6))
    fig.suptitle(f"Fraction of totals (no baselines) - All samples - Average error: {avg_error:.1f}%")
    x_lims = [0, 4.5*10**7]

    ax1.plot(xs, ys, '.', label="Predictions")
    ax1.plot(xs, xs, label="Perfect predictions")
    ax1.plot(xs,p(xs),"r--", label=f"Trendline, R^2 = {r_squared:.3f}")
    ax1.set_title("Estimated energy consumption vs.\nActual energy consumption")
    ax1.legend(loc='upper left')
    ax1.set(xlabel='Actual energy [µJ]', ylabel='Estimated energy [µJ]')
    ax1.set_xlim(x_lims)

    ax2.plot(xs, errors, '.')
    ax2.set_title("Error over actual energy consumption")
    ax2.set(xlabel='Actual energy [µJ]', ylabel='Error [%]')
    ax2.set_xlim(x_lims)

    ax3.hist(xs, bins=50)
    ax3.set_title("Distribution of samples")
    ax3.set(xlabel='Actual energy [µJ]', ylabel='# of sampels')
    ax3.set_xlim(x_lims)
    plt.show()