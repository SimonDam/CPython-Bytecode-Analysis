n = 13631487
min_n = 1
def source_code(n):	
    return f"""#Taken from: https://www.rosettacode.org/wiki/Determine_if_a_string_is_collapsible#Python

from itertools import groupby
import string
import random
random.seed(908376458023859732489752348758796)

def collapser(txt):
    return ''.join(item for item, grp in groupby(txt))
 
def print(*args, **kwargs):
    pass

n = {n}
if __name__ == '__main__':
    strings = [
            "",
            '"If I were two-faced, would I be wearing this one?" --- Abraham Lincoln ',
            "..1111111111111111111111111111111111111111111111111111111111111117777888",
            "I never give 'em hell, I just tell the truth, and they think it's hell. ",
            "                                                   ---  Harry S Truman  ",
            "The better the 4-wheel drive, the further you'll be from help when ya get stuck!",
            "headmistressship",
            "aardvark",
            "😍😀🙌💃😍😍😍🙌",
            ''.join(random.choice(string.ascii_letters) for _ in range(n))
            ]
    for txt in strings:
        this = "Original"
        print(f"\\n{{this:14}} Size: {{len(txt)}} «««{{txt}}»»»" )
        this = "Collapsed"
        sqz = collapser(txt)
        print(f"{{this:>14}} Size: {{len(sqz)}} «««{{sqz}}»»»" )

"""
