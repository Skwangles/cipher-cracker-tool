import random
import math
from utils import *
import sympy
from multiprocessing import Process, Queue
import concurrent.futures
from alive_progress import alive_bar
import rsa_attacks as attacks

RSA_PRIME_MAX = 4_294_967_296 # python's sqrt only works up to this number
RSA_PRIME_MIN = 100_000_000

def generate_weak_key(min=RSA_PRIME_MIN, max=RSA_PRIME_MAX):
    """Generates a weak key, where p and q are close together"""
    [p, q] = get_primes(min, max, True)
    [e, d] = get_d_from_e_mod_n(p, q)
    
    return [p, q, d, e, p*q]


def generate_strong_key(min=RSA_PRIME_MIN, max=RSA_PRIME_MAX):
    """Generates a strong key, where p and q are completely randomly chosen (hopefully not close together)"""
    [p,q] = get_primes(min, max, False)
    [e, d] = get_d_from_e_mod_n(p, q)
    
    return [p, q, d, e, p*q]


def factorise_in_parallel(n):
    """Finds p and q given n, using multiple processes to speed up the search with Fermat's factorisation and brute force"""
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


def crack_n_return_key(n, e, factor_db=True):
    """Finds p, q, and d given n and e"""
    
    p = 0
    q = 0
    d = 0

    if factor_db:
        # Use the factor db to find p and q
        fdb = attacks.factordb_shortcut(n)
        if fdb != None:
            [p, q] = fdb
    
    if p == 0 or q == 0:
        # Use the parallelised attacks to find p and q
        [p, q] = factorise_in_parallel(n)
            
    # Prime factors of n allow us to calculate phi(n) easily
    fi_n = (p-1)*(q-1)
    
    # d is inverse of e mod phi(n)
    d = modInverse(e, fi_n)
    
    if p == 0 or q == 0 or d == 0:
        return None

    return [p, q, d]


def get_d_from_e_mod_n(p, q, e=270679):
    """Given P and Q, calculate the inverse of e mode (p*q) - return d"""
    fi_n = (p-1)*(q-1)
    
    if e > fi_n:
        print("fi_n is too small for default e, generating a new e")
        e = sympy.randprime(2, fi_n)
        
    d = modInverse(e, fi_n)
    return [e, d]


def get_primes(min, max, is_weak=False):
    """Get two prime numbers between min and max, optionally close together"""
    p = sympy.randprime(min, max)
    q = 0
    if is_weak:
        q = sympy.nextprime(sympy.nextprime(p))
    else:
        q = sympy.randprime(min, max)
        while p == q:
            q = sympy.randprime(min, max)
    return [p, q]


def encrypt(m, n, e):                 
    """Encrypts the text using the e and n as a modulus"""
    if m > n:
        # m cannot be larger than N, otherwise it will lose information
        raise ValueError("Message is too long to encrypt with this key")
    
    return pow(m, e, n)


def decrypt(c, n, d):
    """Decrypts the cypher text using the inverse of e mod phi(n)"""
    return pow(c, d, n)


def crack(c, n, e, factor_db=True):
    """Cracks the cypher text, returning the original message"""
    val = crack_n_return_key(n, e, factor_db)
    if val == None:
        return "Could not determine p, q, or d"
    [p, q, d] = val
    
    print("--- Cracked Values ---")
    print("p:", p)
    print("q:", q)
    print("d:", d)
    print("Message:")
    return decrypt(c, n, d)
    
if __name__ == "__main__":
        
    print("Running RSA")
    
    # Generate a key
    # val = generate_strong_key()  #--- test bruteforce
    val = generate_weak_key()
    if val == None:
        print("Could not determine p, q, or d in a reasonable time - please use smaller numbers if you want to crack")
        exit()
    [p, q, d, e, n] = val
    
    print("--- Generated Values ---")
    print("n:", n)
    print("e:", e)
    print("p:", p)
    print("q:", q)
    print("d:", d)
    
    # Encrypt a message
    m = 12
    print("message:", m)
    c = encrypt(m, n, e)
    print("Cipher text:", c)
    
    # Decrypt a message
    print("Decrypted:", decrypt(c, n, d))
    
    # Crack a message
    print("Cracked:", crack(c, n, e, False))
    
