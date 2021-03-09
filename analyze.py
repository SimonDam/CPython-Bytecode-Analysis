from Python.Lib.pathlib import Path
import utils.dataloader as dataloader
from utils.csv_parser import csv_get_values
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
import sys
import baselines.baselines as baselines
from utils.setup import getPython_Paths
import multiprocessing as mp
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

def analysis(measurement_lst, BCT_path, results_lst):
    duration_lst = [x.duration for x in measurement_lst]
    pkg_lst = [sum(x.pkg) for x in measurement_lst]
    dram_lst = [sum(x.dram) for x in measurement_lst]
    
    pkg_fig, pkg_ax = plt.subplots()
    pkg_ax.set_title("Run-time vs. CPU energy consumption.")
    pkg_ax.set_xlabel("Time [µs]")
    pkg_ax.set_ylabel("Energy [µJ]")
    pkg_ax.scatter(duration_lst, pkg_lst)
    pkg_fig.savefig(f"{BCT_path}cpu.pdf")
    pkg_fig.show()

    dram_fig, dram_ax = plt.subplots()
    dram_ax.set_title("Run-time vs. RAM energy consumption.")
    dram_ax.set_xlabel("Time [µs]")
    dram_ax.set_ylabel("Energy [µJ]")
    dram_ax.scatter(duration_lst, dram_lst)
    dram_fig.savefig(f"{BCT_path}ram.pdf")
    dram_fig.show()

    sum_results = {}
    for results in results_lst:
        for key in results['bc_stats']:
            if key in sum_results:
                sum_results[key] += results['bc_stats'][key]
            else:
                sum_results[key] = results['bc_stats'][key]

    # Calculate duration from the average timing of a bytecode, multiplied by the amount of times it has been seen.
    #duration_lst = []
    #for results in results_lst:
    #    duration = 0
    #    for key in results['bc_stats']:
    #        avg = sum_results[key].get_avg()
    #        count = results['bc_stats'][key].count
    #        duration +=  avg * count
    #    duration_lst.append((results['bct_path'], duration, results['duration'], duration / results['duration']))

    sum_dur = 0
    for key in sum_results:
        sum_dur += sum_results[key].timing

    percentage_dict = {}
    for key in sum_results:
        percentage_dict[key] = sum_results[key].timing / sum_dur

    #TODO Calculate the average energy consumption of each bytecode based on the amount of time it takes to execute it, compared to the total time.
    #     Use this to calculate the total energy consumption by simply multiplying the energy consumption of each bytecode with the amount of times it has been executed.

def total_average_of_every_bytecode(bytecode_stat_lst):
    total_dict = {}
    for _, count_sum_dict in bytecode_stat_lst:
        for bytecode in count_sum_dict:
            if bytecode in total_dict:
                total_dict[bytecode]['count'] += count_sum_dict[bytecode]['count']
                total_dict[bytecode]['sum'] += count_sum_dict[bytecode]['sum']
            else:
                total_dict[bytecode] = {'count': count_sum_dict[bytecode]['count'],
                                        'sum': count_sum_dict[bytecode]['sum']}
    
    avg_bytecodes_dict = {}
    for bytecode in total_dict:
        avg_bytecodes_dict[bytecode] = total_dict[bytecode]['sum'] / total_dict[bytecode]['count']

    return avg_bytecodes_dict

def total_count_and_RDTSC_of_bytecodes(count_sum_dict):
    count = 0
    RDTSC = 0
    for bytecode in count_sum_dict:
        count += count_sum_dict[bytecode]['count']
        RDTSC += count_sum_dict[bytecode]['sum']
    return count, RDTSC

def total_energy_and_bytecode_count(bytecode_stat_lst):
    total_energy = 0
    total_count = 0
    total_RDTSC = 0
    for measurement, count_sum_dict in bytecode_stat_lst:
        total_energy += sum(measurement.pkg) + sum(measurement.dram)
        count, RDTSC = total_count_and_RDTSC_of_bytecodes(count_sum_dict)
        total_count += count
        total_RDTSC += RDTSC
        
    return total_energy, total_count, total_RDTSC

def calculate_energy_consumption_by_avg_bytecode(bytecode_stat_lst, avg_dict, RDTSC_overhead = 0, energy_overhead = 0):
    result_lst = []
    total_energy, total_count, total_RDTSC = total_energy_and_bytecode_count(bytecode_stat_lst)
    for measurement, count_sum_dict in bytecode_stat_lst:
        estimated_RDTSC = 0
        for bytecode in count_sum_dict:
            count = count_sum_dict[bytecode]['count']
            avg_bytecode_RDTSC = avg_dict[bytecode] - RDTSC_overhead
            estimated_RDTSC += avg_bytecode_RDTSC * count
        
        estimated_energy = (total_energy * (estimated_RDTSC / total_RDTSC)) - energy_overhead
        actual_energy = sum(measurement.pkg) + sum(measurement.dram)
        result_lst.append((measurement.path_to_data, estimated_energy, actual_energy))

    return result_lst

def get_count_and_sums_for_files_h(path):
    res_dict = {}
    with open(path) as file:
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
    return res_dict


def mp_helper(queue, func, measurement, *args, **kwargs):
    queue.put((measurement, func(*args, **kwargs)))

def get_count_and_sums_for_files(measurement_lst, verbose = False, nr_of_processes = 1):
    if nr_of_processes < 1:
        raise ValueError(f"nr_of_processes must be 1 or above ({nr_of_processes} given).")
    
    bytecode_stat_lst = []
    processes = []
    count = 1

    try:
        queue = mp.Queue()
        while count < len(measurement_lst):
            if len(processes) < nr_of_processes:
                measurement = measurement_lst[count]
                path = measurement.path_to_data
                if verbose: print(f"{len(bytecode_stat_lst)} / {count} / {len(measurement_lst)} : {path}")
                count += 1

                p = mp.Process(target=mp_helper, args=(queue, get_count_and_sums_for_files_h, measurement,  path))
                p.start()
                processes.append(p)
            else:
                for process in processes:
                    if not process.is_alive():
                        processes.remove(process)
                        process.close()

            while not queue.empty():
                bytecode_stat_lst.append(queue.get())
    except KeyboardInterrupt:
        for process in processes:
            process.kill()
            sys.exit()

    return bytecode_stat_lst

def dump_count_sum_lst_to_json(bytecode_stat_lst, dest):
    for measurement, d in bytecode_stat_lst:
        filename = measurement.path_to_data.split(os.sep)[-1]
        with open(Path(f"{dest}/{filename}.json"), 'w') as file:
            json.dump(d, file, indent = 4)

def main():
    vanilla_path, _ = getPython_Paths()

    measurement_lst = dataloader.read_jsons("F:\\BCC data\\small")

    bytecode_stat_lst = get_count_and_sums_for_files(measurement_lst, verbose = True, nr_of_processes = 8)
    dump_count_sum_lst_to_json(bytecode_stat_lst, os.path.abspath("./cache/count_sum"))
    avg_dict = total_average_of_every_bytecode(bytecode_stat_lst)

    RDTSC_baseline = baselines.get_RDTSC()
    empty_baseline = baselines.get_empty(vanilla_path)
    empty_energy = sum(empty_baseline.pkg) + sum(empty_baseline.dram)

    result_lst = calculate_energy_consumption_by_avg_bytecode(bytecode_stat_lst, avg_dict, RDTSC_overhead = RDTSC_baseline, energy_overhead=empty_energy)
    
    with open("result.csv", 'w') as file:
        file.write("path,estimated_energy,actual_energy\n")
        for path, estimated_energy, actual_energy in result_lst:
            file.write(f"\"{path}\",{estimated_energy},{actual_energy}\n")

if __name__ == "__main__":
    main()
