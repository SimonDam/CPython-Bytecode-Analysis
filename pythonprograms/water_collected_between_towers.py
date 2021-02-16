n = 1087
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Water_collected_between_towers#Python

import random
random.seed(87346598389573428956238)

def water_collected(tower):
    N = len(tower)
    highest_left = [0] + [max(tower[:n]) for n in range(1,N)]
    highest_right = [max(tower[n:N]) for n in range(1,N)] + [0]
    water_level = [max(min(highest_left[n], highest_right[n]) - tower[n], 0)
        for n in range(N)]
    print("highest_left:  ", highest_left)
    print("highest_right: ", highest_right)
    print("water_level:   ", water_level)
    print("tower_level:   ", tower)
    print("total_water:   ", sum(water_level))
    print("")
    return sum(water_level)

def print(*args, **kwargs):
    pass

n = {n}

towers = [[1, 5, 3, 7, 2],
    [5, 3, 7, 2, 6, 4, 5, 9, 1, 2],
    [2, 6, 3, 5, 2, 8, 1, 4, 2, 2, 5, 3, 5, 7, 4, 1],
    [5, 5, 5, 5],
    [5, 6, 7, 8],
    [8, 7, 7, 6],
    [6, 7, 10, 7, 6]] + [ [random.randint(1,n) for _ in range(random.randint(4,4+n))] for _ in range(n) ]

[water_collected(tower) for tower in towers]


"""
