from factordb.factordb import FactorDB
from math import ceil, sqrt

def FermatFactors(n): 
   # since fermat's factorization applicable 
   # for odd positive integers only
    if(n<= 0):
        return [n]  
 
    # check if n is a even number 
    if(n & 1) == 0:  
        return [n / 2, 2] 
         
    a = ceil(sqrt(n))
 
    #if n is a perfect root, 
    #then both its square roots are its factors
    if(a * a == n):
        return [a, a]
 
    while(True):
        b1 = a * a - n 
        b = int(sqrt(b1))
        if(b * b == b1):
            break
        else:
            a += 1
    return [int(a-b), int(a + b)]
        

def factordb_shortcut(n):
    """Uses factordb to factorise a number - cheeky shortcut"""
    f = FactorDB(n)
    f.connect()
    match f.get_status():
        case'FF':
            # 'fully factored'
            return f.get_factor_list()
        case _:
            print("Not fully factored")
            return None