import os
import argparse
from pathlib import Path

def _update_file(file_path, destination_path):
    new_text = ""
    if file_path.endswith(".py"):
        found_n = False
        with open(file_path, 'r', encoding="utf8") as file:
            for line in file:
                if line.startswith("n = "):
                    line = "n = {n}\n"
                    found_n = True
                else:
                    if "{" in line or "}" in line:
                        line = line.replace("{", "{{")
                        line = line.replace("}", "}}")
                    if "\\" in line:
                        line = line.replace("\\", "\\\\")
                new_text += line.split("\n")[0]+"\n"

        if found_n:
            new_text = f"def source_code(n):\t\n    return f\"\"\"" + new_text + f"\"\"\"\n"
        else:
            new_text = f"def source_code():\t\n    return f\"\"\"" + new_text + f"\"\"\"\n"

        with open(destination_path, 'w', encoding="utf8") as file:
            file.write(new_text)
    else:
        raise NotImplementedError


def fix(path, destination):
    if os.path.isfile(path):
        filename = path.split(os.sep)[-1]
        _update_file(Path(path), Path(f"{destination}/{filename}"))

    elif os.path.isdir(path):
        dontaskagain = False
        for filename in os.listdir(path):
            destination_path = Path(f"{destination}/{filename}")
            file_exists = os.path.exists(destination_path)

            if file_exists and not dontaskagain:
                answer = input("{destination_path} already exists. Do you want to override (Y / N / Y! / N!). '!' indicates do not ask again.").upper()
                if len(answer) > 2:
                    raise ValueError(f"Invalid answer.")
                if '!' == answer[-1]:
                    dontaskagain = True
                if 'Y' ==  answer[0]:
                    overwrite = True
                if 'N' ==  answer[0]:
                    overwrite = False
                else:
                    raise ValueError(f"Invalid answer.")
            if overwrite or not file_exists:
                _update_file(Path(f"{path}/{filename}"), destination_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path",
                        help="path to a .py-file or directory of .py-files.")
    parser.add_argument("destination", type=float,
                        help="folder to dump the files in.")
    args = parser.parse_args()
    
    print("Warning, running this might not ensure that the file(s) are converted to the string format properly. It only fixes common errors. Preferably convert the file manually.")
    fix(args.path, args.destination)