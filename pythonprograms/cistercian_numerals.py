def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Cistercian_numerals#Python

# -*- coding: utf-8 -*-
'''
Some UTF-8 chars used:
 
‾	8254	203E	&oline;	OVERLINE
┃	9475	2503	 	BOX DRAWINGS HEAVY VERTICAL
╱	9585	2571	 	BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT
╲	9586	2572	 	BOX DRAWINGS LIGHT DIAGONAL UPPER LEFT TO LOWER RIGHT
◸	9720	25F8	 	UPPER LEFT TRIANGLE
◹	9721	25F9	 	UPPER RIGHT TRIANGLE
◺	9722	25FA	 	LOWER LEFT TRIANGLE
◻	9723	25FB	 	WHITE MEDIUM SQUARE
◿	9727	25FF	 	LOWER RIGHT TRIANGLE
 
'''
 
#%% digit sections
 
def _init():
    "digit sections for forming numbers"
    digi_bits = '''
#0  1   2  3  4  5  6   7   8   9
#
 .  ‾   _  ╲  ╱  ◸  .|  ‾|  _|  ◻
#
 .  ‾   _  ╱  ╲  ◹  |.  |‾  |_  ◻
#
 .  _  ‾   ╱  ╲  ◺  .|  _|  ‾|  ◻
#
 .  _  ‾   ╲  ╱  ◿  |.  |_  |‾  ◻
 
'''.strip()
 
    lines = [[d.replace('.', ' ') for d in ln.strip().split()]
             for ln in digi_bits.strip().split('\\n')
             if '#' not in ln]
    formats = '<2 >2 <2 >2'.split()
    digits = [[f"{{dig:{{f}}}}" for dig in line]
              for f, line in zip(formats, lines)]
 
    return digits
 
_digits = _init()
 
 
#%% int to 3-line strings
def _to_digits(n):
    #assert 0 <= n < 10_000 and int(n) == n
 
    return [int(digit) for digit in f"{{int(n):04}}"][::-1]
 
def num_to_lines(n):
    global _digits
    d = _to_digits(n)
    lines = [
        ''.join((_digits[1][d[1]], '┃',  _digits[0][d[0]])),
        ''.join((_digits[0][   0], '┃',  _digits[0][   0])),
        ''.join((_digits[3][d[3]], '┃',  _digits[2][d[2]])),
        ]
 
    return lines
 
def cjoin(c1, c2, spaces='   '):
    return [spaces.join(by_row) for by_row in zip(c1, c2)]

def print(*args, **kwargs):
    pass
#%% main
import random
random.seed(984508945750984257908425960842598067425908672495067)
n = {n}

if __name__ == '__main__':
    #n = 6666
    #print(f"Arabic {{n}} to Cistercian:\\n")
    #print('\\n'.join(num_to_lines(n)))
 
    for pow10 in range(4):    
        step = 10 ** pow10
        print(f'\\nArabic {{step}}-to-{{9*step}} by {{step}} in Cistercian:\\n')
        lines = num_to_lines(step)
        for i in range(step*2, step*10, step):
            lines = cjoin(lines, num_to_lines(i))
        print('\\n'.join(lines))
 
    numbers = [random.randint(1,n) for _ in range(n)]
    print(f'\\nArabic {{str(numbers)[1:-1]}} in Cistercian:\\n')
    lines = num_to_lines(numbers[0])
    for t in numbers[1:]:
        lines = cjoin(lines, num_to_lines(t))
    print('\\n'.join(lines))

"""
