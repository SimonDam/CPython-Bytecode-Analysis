import os
from pathlib import Path
from module_importer import import_module_by_path
import json

def get_ns(filename, json_dict, target_time):
    if filename in json_dict:
        min_max_lst = json_dict[filename]
        for min_max in min_max_lst:
            if target_time is None or target_time == min_max["target_time"]:
                return min_max["n"], min_max["min_n"]
        else:
            print(f"Can't synthesize {filename}, no min/max values matching the target time {target_time}. Consider running min_max.py with that target time.")
            return None
    else:
        print(f"Can't synthesize {filename}, min/max not in min_max.json. Consider looking at min_max.py.")
        return None

def create(source_folder, target_folder, amount, target_time = None):
    try:
        with open(Path(f"{source_folder}/min_max.json"), "r", encoding="utf8") as file:
            json_dict = json.load(file)
    except FileNotFoundError as e:
        raise e(f"Unable synthesize. Missing min_max.json in {source_folder}. Consider running min_max.py.")
    for filename in os.listdir(source_folder):
        if filename.endswith(".py"):
            ns = get_ns(filename, json_dict, target_time)
            if ns is not None:
                n, min_n = ns
            else:
                continue

            filepath = Path(f"{source_folder}/{filename}")
            mod = import_module_by_path(filepath)
            

            delta = (n-min_n)//amount
            if delta < 1:
                delta = 1
            
            n_list = [x for x in range(min_n, n+1, delta)]
            n_list[-1] = n # Ensure that the maximum value was actually used.

            if len(n_list) < amount:
                print(f"Warning: was only able to create {len(n_list)}/{amount} unique files due to min_n {min_n} and n {n} from min_max.json for {filename}.")

            for target_n in n_list:
                source_code = mod.source_code(target_n)
                path, ext = os.path.splitext(filepath)
                name = os.path.basename(path)

                new_filename = Path(f"{name}{target_n}{ext}")
                file_target_folder = Path(f"{target_folder}/{name}/")
                if not os.path.exists(file_target_folder):
                    os.mkdir(file_target_folder)

                with open(Path(f"{file_target_folder}/{new_filename}"), 'w', encoding="utf8") as file:
                    file.write(source_code)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir",
                        help="path to the directory of the .py-files to be synthesized.")
    parser.add_argument("target_dir",
                        help="path to the directory of to dump the synthesized files.")
    parser.add_argument("amount", type=int,
                        help="the amount of files to synthesize per source file. It might not be possible to synthesize this amount due to the values of min_n and n. If this is the case, consider looking at min_max.py.")
    parser.add_argument("--target_time", type=int, default=None,
                        help=f"which target time to look for, when selecting min/max values in min_max.json. If not set, will just take the first min/max values.")
    
    args = parser.parse_args()
    create(args.source_dir, args.target_dir, args.amount, target_time=args.target_time)
