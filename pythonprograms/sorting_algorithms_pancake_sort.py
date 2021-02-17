n = 1119
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Pancake_sort#Python

tutor = False
 
def pancakesort(data):
    if len(data) <= 1:
        return data
    if tutor: print()
    for size in range(len(data), 1, -1):
        maxindex = max(range(size), key=data.__getitem__)
        if maxindex+1 != size:
            # This indexed max needs moving
            if maxindex != 0:
                # Flip the max item to the left
                if tutor: print('With: %r doflip  %i'
                                % ( ' '.join(str(x) for x in data), maxindex+1 ))
                data[:maxindex+1] = reversed(data[:maxindex+1])
            # Flip it into its final position
            if tutor: print('With: %r  doflip %i'
                                % ( ' '.join(str(x) for x in data), size ))
            data[:size] = reversed(data[:size])
    if tutor: print()


def print(*args, **kwargs):
    pass
n = {n}

if __name__ == '__main__':
    import random
    random.seed(657834598756438976598432658723465897)

    tutor = True
    data = list(str(list(range(n))))
    while data == sorted(data):
        random.shuffle(data)
    print('Original List: %r' % ' '.join(data))
    pancakesort(data)
    print('Pancake Sorted List: %r' % ' '.join(data))

"""
