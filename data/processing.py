import baselines.baselines as baselines
import utils.setup

import data.fraction_of_total.helpers as fot

def fraction_of_totals(bytecode_stat_lst, use_baselines = True):
    avg_dict = fot.averages(bytecode_stat_lst)

    vanilla_path, _ = utils.setup.getPython_Paths()
    if use_baselines:
        RDTSC_baseline = baselines.get_RDTSC()
        empty_baseline = baselines.get_empty(vanilla_path)
    else:
        RDTSC_baseline = 0
        empty_baseline = 0
    empty_energy = sum(empty_baseline.pkg) + sum(empty_baseline.dram)
    return fot.results(bytecode_stat_lst, avg_dict, RDTSC_overhead=RDTSC_baseline, energy_overhead=empty_energy)
