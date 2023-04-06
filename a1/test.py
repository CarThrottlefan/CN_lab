a = 1

def sum(): 
    global a # needed to modify the global value of a
    a += 2

sum()
print(a)