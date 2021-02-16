n = 12650140831706913647030959169932331690597290610258882397306334876714396222999709180747523981339820280949192366519800744461863046086612092304188337496296156870094839017285397585279181733880826021327485479904546566785125467714043293663631459728072472271300628532022423097020838413451906408261645469290375391456731733818343423
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Peaceful_chess_queen_armies#Python

from itertools import combinations, product, count
from functools import lru_cache, reduce
 
 
_bbullet, _wbullet = '\\u2022\\u25E6'
_or = set.__or__
 
def place(m, n):
    "Place m black and white queens, peacefully, on an n-by-n board"
    board = set(product(range(n), repeat=2))  # (x, y) tuples
    placements = {{frozenset(c) for c in combinations(board, m)}}
    for blacks in placements:
        black_attacks = reduce(_or, 
                               (queen_attacks_from(pos, n) for pos in blacks), 
                               set())
        for whites in {{frozenset(c)     # Never on blsck attacking squares
                       for c in combinations(board - black_attacks, m)}}:
            if not black_attacks & whites:
                return blacks, whites
    return set(), set()
 
@lru_cache(maxsize=None)
def queen_attacks_from(pos, n):
    x0, y0 = pos
    a = set([pos])    # Its position
    a.update((x, y0) for x in range(n))    # Its row
    a.update((x0, y) for y in range(n))    # Its column
    # Diagonals
    for x1 in range(n):
        # l-to-r diag
        y1 = y0 -x0 +x1
        if 0 <= y1 < n: 
            a.add((x1, y1))
        # r-to-l diag
        y1 = y0 +x0 -x1
        if 0 <= y1 < n: 
            a.add((x1, y1))
    return a
 
def pboard(black_white, n):
    "Print board"
    if black_white is None: 
        blk, wht = set(), set()
    else:
        blk, wht = black_white
    print(f"## {{len(blk)}} black and {{len(wht)}} white queens "
          f"on a {{n}}-by-{{n}} board:", end='')
    for x, y in product(range(n), repeat=2):
        if y == 0:
            print()
        xy = (x, y)
        ch = ('?' if xy in blk and xy in wht 
              else 'B' if xy in blk
              else 'W' if xy in wht
              else _bbullet if (x + y)%2 else _wbullet)
        print('%s' % ch, end='')
    print()

def print(*args, **kwargs):
    pass

n = {n}
if __name__ == '__main__':
    i=2
    for i in range(2, 6):
        print()
        for m in count(1):
            ans = place(m, i)
            if ans[0]:
                pboard(ans, i)
            else:
                print (f"# Can't place {{m}} queens on a {{i}}-by-{{i}} board")
                break
    #
    print('\\n')
    m, i = 5, 7
    ans = place(m, i)
    pboard(ans, i)


"""
