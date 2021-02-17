n = 20971519
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Bioinformatics/Sequence_mutation#Python

import random
random.seed(98237640983264587934897532489752348975623487)
from collections import Counter
 
def basecount(dna):
    return sorted(Counter(dna).items())
 
def seq_split(dna, n=50):
    return [dna[i: i+n] for i in range(0, len(dna), n)]
 
def seq_pp(dna, n=50):
    for i, part in enumerate(seq_split(dna, n)):
        print(f"{{i*n:>5}}: {{part}}")
    print("\\n  BASECOUNT:")
    tot = 0
    for base, count in basecount(dna):
        print(f"    {{base:>3}}: {{count}}")
        tot += count
    base, count = 'TOT', tot
    print(f"    {{base:>3}}= {{count}}")
 
def seq_mutate(dna, count=1, kinds="IDSSSS", choice="ATCG" ):
    mutation = []
    k2txt = dict(I='Insert', D='Delete', S='Substitute')
    for _ in range(count):
        kind = random.choice(kinds)
        index = random.randint(0, len(dna))
        if kind == 'I':    # Insert
            dna = dna[:index] + random.choice(choice) + dna[index:]
        elif kind == 'D' and dna:  # Delete
            dna = dna[:index] + dna[index+1:]
        elif kind == 'S' and dna:  # Substitute
            dna = dna[:index] + random.choice(choice) + dna[index+1:]
        mutation.append((k2txt[kind], index))
    return dna, mutation

def print(*args, **kwargs):
    pass

n = {n}
if __name__ == '__main__':
    print("SEQUENCE:")
    sequence = ''.join(random.choices('ACGT', weights=(1, 0.8, .9, 1.1), k=n))
    seq_pp(sequence)
    print("\\n\\nMUTATIONS:")
    mseq, m = seq_mutate(sequence, 10)
    for kind, index in m:
        print(f" {{kind:>10}} @{{index}}")
    print()
    seq_pp(mseq)

"""
