def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Spiral_matrix#Python

def spiral(n):
    dx,dy = 1,0            # Starting increments
    x,y = 0,0              # Starting location
    myarray = [[None]* n for j in range(n)]
    for i in range(n**2):
        myarray[x][y] = i
        nx,ny = x+dx, y+dy
        if 0<=nx<n and 0<=ny<n and myarray[nx][ny] == None:
            x,y = nx,ny
        else:
            dx,dy = -dy,dx
            x,y = x+dx, y+dy
    return myarray
 
def printspiral(myarray):
    n = range(len(myarray))
    for y in n:
        for x in n:
            print("%2i" % myarray[x][y], end = " ")
        print()
 
def print(*args, **kwargs):
    pass

n = {n}
printspiral(spiral(n))

"""
