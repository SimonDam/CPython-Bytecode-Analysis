import utils.dataloader as dataloader
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import json
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

def calculate_average_of_every_bytecode(data_lst):
    avg_bytecodes_dict = {}
    count = 0
    for data_df in data_lst:
        print(count, '/', len(data_lst))
        count+=1
        for chunk in data_df:
            for _, bytecode, value in chunk.itertuples():
                if bytecode not in avg_bytecodes_dict:
                    avg_bytecodes_dict[bytecode] = {"sum":value, "count":1}
                else:
                    avg_bytecodes_dict[bytecode]["sum"] += value
                    avg_bytecodes_dict[bytecode]["count"] += 1
            
    for key in avg_bytecodes_dict:
        avg = avg_bytecodes_dict[key]["sum"] / avg_bytecodes_dict[key]["count"]
        avg_bytecodes_dict[key] = avg
    
    return avg_bytecodes_dict

def calculate_energy_consumption_by_avg_bytecode(data_lst, measurement_lst):
    with open("avg.json", 'r') as file:
        avg_dict = json.load(file)
    sum_lst = []
    count = 0
    for data_df in data_lst:
        sum_of_values = 0
        print(count, "/", len(data_lst))
        for chunk in data_df:
            for _, bytecode, _ in chunk.itertuples():
                sum_of_values += avg_dict[str(bytecode)]
        sum_lst.append(sum_of_values)
    
    for measurement, sum_value in zip(measurement_lst, sum_lst):
        energy = sum(measurement.pkg) + sum(measurement.dram)
        print(f"energy: {energy}, sum_value: {sum_value}")

def main():
    measurement_lst = dataloader.read_jsons("/home/simon/Desktop/bcc")
    csv_paths = [x.path_to_data for x in measurement_lst]
    
    data_lst = []
    for path in csv_paths:
        data_lst.append(pd.read_csv(path, engine = 'c', sep = ',', chunksize = 10**9))
    
    print(calculate_energy_consumption_by_avg_bytecode(data_lst, measurement_lst))

if __name__ == "__main__":
    main()
