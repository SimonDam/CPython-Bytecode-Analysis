# Taken from: https://www.rosettacode.org/wiki/Dutch_national_flag_problem#Python

import random
random.seed(387408934580973458023465637485873456)

def print(*args, **kwargs):
    pass

colours_in_order = 'Red White Blue'.split()
 
def dutch_flag_sort(items, order=colours_in_order):
    'return sort of items using the given order'
    reverse_index = dict((x,i) for i,x in enumerate(order))
    return sorted(items, key=lambda x: reverse_index[x])
 
def dutch_flag_check(items, order=colours_in_order):
    'Return True if each item of items is in the given order'
    reverse_index = dict((x,i) for i,x in enumerate(order))
    order_of_items = [reverse_index[item] for item in items]
    return all(x <= y for x, y in zip(order_of_items, order_of_items[1:]))
 
def random_balls(mx=5):
    'Select from 1 to mx balls of each colour, randomly'
    balls = sum([[colour] * random.randint(1, mx)
                 for colour in colours_in_order], [])
    random.shuffle(balls)
    return balls
 
def main(n):
    # Ensure we start unsorted
    while True:
        balls = random_balls(mx = n)
        if not dutch_flag_check(balls):
            break
    print("Original Ball order:", balls)
    sorted_balls = dutch_flag_sort(balls)
    print("Sorted Ball Order:", sorted_balls)
    assert dutch_flag_check(sorted_balls), 'Whoops. Not sorted!'

n = 4500000
if __name__ == '__main__':
    main(n)

