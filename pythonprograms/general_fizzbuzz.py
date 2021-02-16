n = 10485759
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/General_FizzBuzz#Python

def genfizzbuzz(factorwords, numbers):
    factorwords.sort(key=lambda p: p[0])
    lines = []
    for num in numbers:
        words = ''.join(wrd for fact, wrd in factorwords if (num % fact) == 0)
        lines.append(words if words else str(num))
    return '\\n'.join(lines)
 
def print(*args, **kwargs):
    pass


n = {n}
if __name__ == '__main__':
    print(genfizzbuzz([(5, 'Buzz'), (3, 'Fizz'), (7, 'Baxx')], range(1, n)))

"""
