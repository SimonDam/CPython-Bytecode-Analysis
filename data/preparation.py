import random

from utils.bytecodes import valid_bytecodes_set
import numpy as np


def prepare_data(bytecode_stat_lst):
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
    arr = np.zeros(len(valid_bytecodes_set))
    for i, key in enumerate(dict):
        # We are subtracting here since the first smallest valid bytecode is 1.
        # Avoids going out of bounds.
        value = dict[key]
        arr[i] = value["count"]
    return arr

def split_train_val_test(data, train_split, val_split, shuffle = True, seed = None):
    n = len(data)
    train_end = round(n * train_split)
    val_end = train_end + round(n * val_split)

    train = data[:train_end]
    val = data[train_end:val_end]
    test = data[val_end:]

    if shuffle:
        if seed is not None:
            random.seed(seed)
        random.shuffle(train)
        random.shuffle(val)
        random.shuffle(test)
    return train, val, test