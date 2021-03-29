import json
import os
from pathlib import Path
import random
import data.preparation as preparation

from utils.measurement import Measurement

def read_jsons(path, max_number = None, shuffle = True, seed = None):
    measurement_lst = []
    files = os.listdir(path)
    if shuffle:
        if seed is not None:
            random.seed(seed)
        random.shuffle(files)
    for filename in files:
        if filename.endswith(".json"):
            with open(Path(f"{path}/{filename}")) as file:
                data_dict = json.load(file)
                if not os.path.exists(data_dict["bct_path"]):
                    raise FileNotFoundError(f"{data_dict['bct_path']} specified in {path}/{filename} does exist at that location.")

                if max_number is not None:
                    if len(measurement_lst) > max_number:
                        return measurement_lst

                # TODO use the measurement_to_dict function instead.
                duration = data_dict["duration"]
                pkg = data_dict["pkg"]
                dram = data_dict["dram"]
                path_to_data = data_dict["bct_path"]
                measurement_lst.append((Measurement(duration, pkg, dram, path_to_data = path_to_data), data_dict))
    return measurement_lst

def read_from_folders(path, samples_per_folder = (None, None, None), train_split = None, val_split = None, shuffle = True, seed = None):
    train_split, val_split = _verify_splits(train_split, val_split)
    folders = os.listdir(path)
    train_folders, val_folders, test_folders = preparation.split_train_val_test(folders, train_split, val_split, shuffle=shuffle, seed=seed)

    train_samples, val_samples, test_samples = samples_per_folder

    result_train = _read_from_folders_h(train_folders, path, train_samples, shuffle, seed)
    result_val = _read_from_folders_h(val_folders, path, val_samples, shuffle, seed)
    result_test = _read_from_folders_h(test_folders, path, test_samples, shuffle, seed)

    return result_train, result_val, result_test

def _read_from_folders_h(folders, path, samples_per_folder, shuffle, seed):
    result_lst = []
    for folder in folders:
        folder_path = Path(f"{path}/{folder}")
        if os.path.isdir(folder_path):
            result_lst += read_jsons(folder_path, max_number=samples_per_folder, shuffle=shuffle, seed=seed)
    return result_lst

def _verify_splits(train_split, val_split):
    if train_split is not None:
        if not isinstance(train_split, (int, float)):
            raise TypeError(f"train_split {train_split} must be of type float or int.")
        if not (0 < train_split < 1):
            raise ValueError(f"train_split {train_split} must be between 0 and 1.")
    else:
        if val_split is None:
            raise TypeError(f"If train_split is None, then val_split must also be None, {val_split} given.")
        train_split = 1

    if val_split is not None:
        if not isinstance(val_split, (int, float)):
            raise TypeError(f"val_split {val_split} must be of type float or int.")
        if not (0 < val_split < 1):
            raise ValueError(f"val_split {val_split} must be between 0 and 1.")
        if train_split + val_split > 1:
            raise ValueError(f"train_split + val_split {train_split + val_split} must be between 0 and 1.")
    else:
        val_split = 0
    return train_split, val_split