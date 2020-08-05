# Calculates the first 10.000 fibbonaci numbers
f1 = 1
f2 = 1
for i in range(10000):
    f1, f2 = f2, f1+f2
