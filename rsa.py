import random
import math
import utils
import sympy
from multiprocessing import Process, Queue
import concurrent.futures
from alive_progress import alive_bar
import rsa_attacks as attacks

RSA_PRIME_MAX = 4_294_967_296 # python's sqrt only works up to this number
RSA_PRIME_MIN = 100_000_000

def generate_weak_key(min=RSA_PRIME_MIN, max=RSA_PRIME_MAX):
    p = sympy.randprime(min, max)
    q = sympy.nextprime(sympy.nextprime(p))
    while p == q:
        q = sympy.randprime(min, max)
    
    fi_n = (p-1)*(q-1)
    
    # small enough so that m^e is < n  - ideally 65537
    e = 11
    if e > fi_n:
        print("fi_n is too small for default e, generating a new e")
        e = sympy.randprime(2, fi_n)
        
    d = utils.modInverse(e, fi_n)

    print("e:", e)
    print("n:", p*q)
    
    return [p, q, d]

def find_prime_parallel(n):
    result_queue = Queue()

    # multiprocess the attacks
    processes = [Process(target=attacks.fermat, args=(n, result_queue)), Process(target=attacks.bruteforce, args=(n, result_queue))]

    for process in processes:
        process.start()

    # wait for a result from any of the processes
    result = result_queue.get()

    while result is None:
        if not any(process.is_alive() for process in processes):
            raise Exception("No result found, all attacks exhausted...")
        result = result_queue.get()
        
    # solution is found, don't need to continue more attacks
    for process in processes:
        if process.is_alive():
            process.terminate()
            
    return result


def find_p_q_d(n, e):
    """Finds p, q, and d given n and e"""
    
    p = 0
    q = 0
    d = 0

    fdb = attacks.factordb_shortcut(n)
    if fdb != None:
        [p, q] = fdb
    else:
        [p, q] = find_prime_parallel(n)
    
            
    # Find d
    fi_n = (p-1)*(q-1)
    d = utils.modInverse(e, fi_n)
    
    if p == 0 or q == 0 or d == 0:
        return None

    return [p, q, d]




def encrypt(m, n, e):                 
    """Encrypts the text using the key"""
    if pow(m, e) > n:
        # m^e cannot be larger than N, otherwise it will lose information
        raise ValueError("Message is too long to encrypt with this key")
    
    return pow(m, e, n)


def decrypt(c, n, d):
    """Decrypts the cypher text using the key"""
    return pow(c, d, n)


def crack(c, n, e):
    """Cracks the cypher text, returning the key"""
    val = find_p_q_d(n, e)
    if val == None:
        return "Could not determine p, q, or d"
    [p, q, d] = val
    print("p:", p)
    print("q:", q)
    print("d:", d)
    return decrypt(c, n, d)
    
if __name__ == "__main__":
        
    print("Running RSA")
    
    # Generate a key
    val = generate_weak_key()
    if val == None:
        print("Could not determine p, q, or d in a reasonable time - please use smaller numbers if you want to crack")
        exit()
    [p, q, d] = val
    print("p:", p)
    print("q:", q)
    print("d:", d)
    
    e = utils.modInverse(d, (p-1)*(q-1))
    
    # Encrypt a message
    m = 12
    print("message:", m)
    c = encrypt(m, p*q, e)
    print("Cipher text:", c)
    
    # Decrypt a message
    print("Decrypted:", decrypt(c, p*q, d))
    
    # Crack a message
    print("Cracked:", crack(c, p*q, e))
    
