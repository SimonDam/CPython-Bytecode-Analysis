def source_code(n):	
    return f"""# Written by Simon Dam Nielsen

n = {n}

f1 = 1
f2 = 1
for i in range(n):
    f1, f2 = f2, f1+f2


"""
