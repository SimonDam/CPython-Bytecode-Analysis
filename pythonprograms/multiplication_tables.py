def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Multiplication_tables#Python

def print(*args, **kwargs):
    pass

n = {n}

size = n
width = len(str(size**2))
for row in range(-1,size+1):
    if row==0:
        print("─"*width + "┼"+"─"*((width+1)*size-1))
    else:
        print("".join("%*s%1s" % ((width,) + (("x","│")      if row==-1 and col==0
                                  else (row,"│") if row>0   and col==0
                                  else (col,"")  if row==-1
                                  else ("","")   if row>col
                                  else (row*col,"")))
                   for col in range(size+1)))

"""
