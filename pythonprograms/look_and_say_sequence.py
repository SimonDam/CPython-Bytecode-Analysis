n = 59
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Look-and-say_sequence#Python

def lookandsay(number):
    result = ""
 
    repeat = number[0]
    number = number[1:]+" "
    times = 1
 
    for actual in number:
        if actual != repeat:
            result += str(times)+repeat
            times = 1
            repeat = actual
        else:
            times += 1
 
    return result
 
num = "1"

def print(*args, **kwargs):
    pass

n = {n}
for i in range(n):
    print(num)
    num = lookandsay(num)

"""
