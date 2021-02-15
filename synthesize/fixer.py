import os

def main():
    print(os.listdir("."))
    for program in os.listdir("./pythonprograms"):
        new_text = ""
        if program.endswith(".py"):
            found_n = False
            with open(f".\\pythonprograms\\{program}", 'r', encoding="utf8") as file:
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
            
            with open(f".\\fixed\\{program}", 'w', encoding="utf8") as file:
                file.write(new_text)
    
if __name__ == "__main__":
    main()