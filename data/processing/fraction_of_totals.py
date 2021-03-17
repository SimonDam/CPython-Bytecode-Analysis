import baselines.baselines as baselines
import utils.setup

def get_results(bytecode_stat_lst, use_baselines = True):
    avg_dict = _averages(bytecode_stat_lst)

    vanilla_path, _ = utils.setup.getPython_Paths()
    if use_baselines:
        RDTSC_baseline = baselines.get_RDTSC()
        empty_baseline = baselines.get_empty(vanilla_path)
    else:
        RDTSC_baseline = 0
        empty_baseline = 0
    empty_energy = sum(empty_baseline.pkg) + sum(empty_baseline.dram)
    return _results(bytecode_stat_lst, avg_dict, RDTSC_overhead=RDTSC_baseline, energy_overhead=empty_energy)

def _results(bytecode_stat_lst, avg_dict, RDTSC_overhead = 0, energy_overhead = 0):
    result_lst = []
    total_energy, total_count, total_RDTSC = _totals(bytecode_stat_lst)
    
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

def _averages(bytecode_stat_lst):
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

def _totals(bytecode_stat_lst):
    total_energy = 0
    total_count = 0
    total_RDTSC = 0
    for measurement, count_sum_dict in bytecode_stat_lst:
        total_energy += sum(measurement.pkg) + sum(measurement.dram)
        count, RDTSC = _total_count_and_RDTSC_of_bytecodes(count_sum_dict)
        total_count += count
        total_RDTSC += RDTSC
    
    return total_energy, total_count, total_RDTSC

def _total_count_and_RDTSC_of_bytecodes(count_sum_dict):
    count = 0
    RDTSC = 0
    for bytecode in count_sum_dict:
        count += count_sum_dict[bytecode]['count']
        RDTSC += count_sum_dict[bytecode]['sum']
    return count, RDTSC

