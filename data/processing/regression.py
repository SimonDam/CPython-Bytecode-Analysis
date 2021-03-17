import numpy as np
from sklearn.linear_model import LinearRegression
from utils.bytecodes import valid_bytecodes_set


def get_results(bytecode_stat_lst):
    measurement_paths, xs, ys = _prepare_data(bytecode_stat_lst)
    result_arr = _predict(xs, ys)
    return list(zip(measurement_paths, list(result_arr), list(ys)))

def _prepare_data(bytecode_stat_lst):
    measurement_paths = []
    xs = []
    ys = []
    for measurement, count_sum_dict in bytecode_stat_lst:
        pkg_lst = measurement.pkg
        dram_lst = measurement.dram
        measurement_paths.append(measurement.path_to_data)
        ys.append(sum(pkg_lst) + sum(dram_lst))
        xs.append(_dict_to_numpy(count_sum_dict))
    return measurement_paths, xs, ys

def _dict_to_numpy(dict):
    arr = np.zeros(max(valid_bytecodes_set))
    for key, value in dict.items():
        # We are subtracting here since the first smallest valid bytecode is 1.
        # Avoids going out of bounds.
        arr[int(key)-1] = value["count"]
    return arr

def _predict(xs, ys):
    reg = LinearRegression().fit(xs, ys)
    return reg.predict(xs)
