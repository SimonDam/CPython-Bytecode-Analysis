# Prints the first 10.000 fibbonaci numbers
f1 = 1
f2 = 1
for i in range(10000):
    print(i, f1)
    f1, f2 = f2, f1+f2
