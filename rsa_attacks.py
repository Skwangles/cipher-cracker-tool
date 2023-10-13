from factordb.factordb import FactorDB
import os
from math import ceil, sqrt

def fermat(n, result_queue): 
    """Fermat's factorisation method - https://en.wikipedia.org/wiki/Fermat%27s_factorization_method"""

    if n <= 0:
        raise Exception("n must be greater than 0")
 
    # if n is even, we already know a factor 
    if n % 2 == 0:  
        result_queue.put([int(n//2), int(2)])
        return
         
    a = ceil(sqrt(n))
 
    # if n is a perfect square, we already know the factors
    if(a * a == n):
        result_queue.put([int(a), int(a)])
        return
 
    while True:
        b1 = a * a - n 
        b = int(sqrt(b1))
        if(b * b == b1):
            break
        else:
            a += 1
    
    print("Fermat factorization method success!")
    result_queue.put([int(a-b), int(a + b)])
        

def factordb_shortcut(n):
    """Uses factordb to factorise a number - cheeky shortcut"""
    f = FactorDB(n)
    f.connect()
    match f.get_status():
        case'FF':
            # 'fully factored'
            print("FactorDB method success!")
            return f.get_factor_list()
        case _:
            print("Not fully factored:" + f.get_status() + " - continuing...")
            return None
   

def check_file(name: str, n: int):
    """Checks a file for factors of n, loading all the primes into memory"""
    primes = open(name, "r")
    n_sqrt = sqrt(n)
    
    # check every line in the file
    for line in primes:
        num = int(line)
        if n % num == 0:
            return [num, n//num]
        
        if num > n_sqrt:
            primes.close()
            return None
        
    # clean up and indicate we've reached the end of the file
    primes.close()
    return []

     
def bruteforce(n, result_queue):
    primes_path = "primes/"
    file_list = [primes_path + str(f) for f in os.listdir(primes_path)]
    for file in file_list:
        primes = check_file(file, n)
        if primes == None:
            # Reached > sqrt_n
            result_queue.put(None)
            return
        if primes != []:
            print("Bruteforce method success!")
            result_queue.put(primes)
            return
        
    print("Bruteforce: Primes are larger than we have files for...")
    result_queue.put(None)


