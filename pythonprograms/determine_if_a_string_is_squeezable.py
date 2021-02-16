n = 10485759
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Determine_if_a_string_is_squeezable#Python

from itertools import groupby
import string
import random
random.seed(123873624987326428795629876452)

def print(*args, **kwargs):
    pass

def squeezer(s, txt):
    return ''.join(item if item == s else ''.join(grp)
                   for item, grp in groupby(txt))
 
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
            ''.join((random.choice(string.ascii_letters)) for _ in range(n))
            ]
    squeezers = f' ,-,7,., -r,e,s,a,😍,{{random.choice(string.ascii_letters)}}'.split(',')
    for txt, chars in zip(strings, squeezers):
        this = "Original"
        print(f"\\n{{this:14}} Size: {{len(txt)}} «««{{txt}}»»»" )
        for ch in chars:
            this = f"Squeezer '{{ch}}'"
            sqz = squeezer(ch, txt)
            print(f"{{this:>14}} Size: {{len(sqz)}} «««{{sqz}}»»»" )

"""
