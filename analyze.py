import argparse
import json
import multiprocessing as mp
import os
import sys

import utils.dataloader as dataloader
from data import processing
from Python.Lib.pathlib import Path
from utils.csv_parser import csv_get_values


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
    measurement_lst = dataloader.read_jsons(args.folder)
    bytecode_stat_lst = get_count_and_sums_for_files(measurement_lst, verbose = args.verbose, nr_of_processes = args.processes, force = args.force)

    # Analyze data
    result_lst = processing.fraction_of_totals(bytecode_stat_lst, use_baselines = (not args.force))
    
    with open("result.csv", 'w') as file:
        file.write("path,estimated_energy,actual_energy\n")
        for path, estimated_energy, actual_energy in result_lst:
            file.write(f"\"{path}\",{estimated_energy},{actual_energy}\n")