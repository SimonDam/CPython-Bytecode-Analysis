n = 8194
min_n = 4
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Bubble_sort#Python

def bubble_sort(seq):
    '''Inefficiently sort the mutable sequence (list) in place.
       seq MUST BE A MUTABLE SEQUENCE.
 
       As with list.sort() and random.shuffle this does NOT return 
    '''
    changed = True
    while changed:
        changed = False
        for i in range(len(seq) - 1):
            if seq[i] > seq[i+1]:
                seq[i], seq[i+1] = seq[i+1], seq[i]
                changed = True
    return seq

n = {n}

if __name__ == "__main__":
   '''Sample usage and simple test suite'''
 
   from random import shuffle, seed
   seed(934759834576984)
 
   testset = list(range(n))
   testcase = testset[:] # make a copy
   shuffle(testcase)
   assert testcase != testset  # we've shuffled it
   bubble_sort(testcase)
   assert testcase == testset  # we've unshuffled it back into a copy

"""
