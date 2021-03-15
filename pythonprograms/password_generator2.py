def source_code(n):	
    return f"""# Written by Simonm Dam Nielsen

import random
import string

def main(n):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for _ in range(n):
        password += random.choice(characters)

random.seed(8764359826387563248975623487956)
n = {n}
if __name__ == "__main__":
    main(n)


"""
