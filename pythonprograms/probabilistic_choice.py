n = 7340031
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Probabilistic_choice#Python

import random, bisect
 
def probchoice(items, probs):
  '''\\
  Splits the interval 0.0-1.0 in proportion to probs
  then finds where each random.random() choice lies
  '''
 
  prob_accumulator = 0
  accumulator = []
  for p in probs:
    prob_accumulator += p
    accumulator.append(prob_accumulator)
 
  while True:
    r = random.random()
    yield items[bisect.bisect(accumulator, r)]
 
def probchoice2(items, probs, bincount=10000):
  '''\\
  Puts items in bins in proportion to probs
  then uses random.choice() to select items.
 
  Larger bincount for more memory use but
  higher accuracy (on avarage).
  '''
 
  bins = []
  for item,prob in zip(items, probs):
    bins += [item]*int(bincount*prob)
  while True:
    yield random.choice(bins)
 
 
def tester(func=probchoice, items='good bad ugly'.split(),
                    probs=[0.5, 0.3, 0.2],
                    trials = 100000
                    ):
  def problist2string(probs):
    '''\\
    Turns a list of probabilities into a string
    Also rounds FP values
    '''
    return ",".join('%8.6f' % (p,) for p in probs)
 
  from collections import defaultdict
 
  counter = defaultdict(int)
  it = func(items, probs)
  for dummy in range(trials):
    counter[it.__next__()] += 1
  print("\\n##\\n## %s\\n##" % func.__name__.upper()  )
  print("Trials:              ", trials)
  print("Items:               ", ' '.join(items))
  print("Target probability:  ", problist2string(probs))
  print("Attained probability:", problist2string(
    counter[x]/float(trials) for x in items))

def print(*args, **kwargs):
    pass

random.seed(93847502347580923470589324876)
n = {n}

if __name__ == '__main__':
  items = 'aleph beth gimel daleth he waw zayin heth'.split()
  probs = [1/(float(t)+5) for t in range(len(items))]
  probs[-1] = 1-sum(probs[:-1])
  tester(probchoice, items, probs, n)
  tester(probchoice2, items, probs, n)

"""
