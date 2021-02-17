n = 2359295
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Count_the_coins#Python

def count_changes(amount_cents, coins):
    n = len(coins)
    # max([]) instead of max() for Psyco
    cycle = max([c+1 for c in coins if c <= amount_cents]) * n
    table = [0] * cycle
    for i in range(n):
        table[i] = 1
 
    pos = n
    for s in range(1, amount_cents + 1):
        for i in range(n):
            if i == 0 and pos >= cycle:
                pos = 0
            if coins[i] <= s:
                q = pos - coins[i] * n
                table[pos]= table[q] if (q >= 0) else table[q + cycle]
            if i:
                table[pos] += table[pos - 1]
            pos += 1
    return table[pos - 1]

def print(*args, **kwargs):
    pass

n = {n}
def main():
    us_coins = [100, 50, 25, 10, 5, 1]
    eu_coins = [200, 100, 50, 20, 10, 5, 2, 1]
    for coins in (us_coins, eu_coins):
        print(count_changes(n, coins[2:]))
 
main()

"""
