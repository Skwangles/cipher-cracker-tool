import random
import math
import utils
import sympy

RSA_PRIME_MAX = 10_000
RSA_PRIME_MIN = 1000

def generate_key(min=RSA_PRIME_MIN, max=RSA_PRIME_MAX):
    p = sympy.randprime(min, max)
    q = sympy.randprime(min, max)
    while p == q:
        q = sympy.randprime(min, max)
    
    fi_n = (p-1)*(q-1)
    
    e = 65537 # generally a good choice
    
    d = utils.modInverse(e, fi_n)

    print("e:", e)
    print("n:", p*q)
    
    return [p, q, d]


def find_p_q_d(n, e):
    """Finds p, q, and d given n and e"""
    p = 0
    q = 0
    d = 0
    
    # Find p and q - first check primes close to sqrt(n)
    for i in range(int(math.sqrt(n)), 2, -2):
        if n % i == 0:
            p = i
            q = n // i
            break
    
    # Find d
    fi_n = (p-1)*(q-1)
    d = utils.modInverse(e, fi_n)
    
    if p == 0 or q == 0 or d == 0:
        return "Could not find p, q, and d"

    return [p, q, d]


def encrypt(m, n, e, p, q):                 
    """Encrypts the text using the key"""
    if p or q:
        return pow(m, e, p*q)
    return pow(m, e, n)


def decrypt(c, n, d):
    """Decrypts the cypher text using the key"""
    return pow(c, d, n)


def crack(c, n, e):
    """Cracks the cypher text, returning the key"""
    [p,q, d] = find_p_q_d(n, e)
    print("p:", p)
    print("q:", q)
    print("d:", d)
    return decrypt(c, n, d)
    
if __name__ == "__main__":
        
    print("Running RSA")
    
    # Generate a key
    [p, q, d] = generate_key()
    print("p:", p)
    print("q:", q)
    print("d:", d)
    
    # p = 5
    # q = 11
    # d = 27
    
    e = utils.modInverse(d, (p-1)*(q-1))
    
    # Encrypt a message
    m = 2
    print("message:", m)
    c = encrypt(m, p*q, e)
    print("Cipher text:", c)
    
    # Decrypt a message
    print("Decrypted:", decrypt(c, p*q, d))
    
    # Crack a message
    print("Cracked:", crack(c, p*q, e))
    
    
