import random
import math
import utils
import sympy
from alive_progress import alive_bar

RSA_PRIME_MAX = 100_000_000
RSA_PRIME_MIN = 100_000

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
    sqrt_n = int(math.sqrt(n))
    if sqrt_n % 2 == 0: # make sure sqrt_n is odd, so we can decrement by 2
        sqrt_n += 1 
        
    with alive_bar(sqrt_n//2) as bar:
        for i in range(sqrt_n, 2, -2):
            if n % i == 0:
                p = i
                q = n // i
                break
            bar()
    
    # Find d
    fi_n = (p-1)*(q-1)
    d = utils.modInverse(e, fi_n)
    
    if p == 0 or q == 0 or d == 0:
        return None

    return [p, q, d]


def encrypt(m, n, e, p=None, q=None):                 
    """Encrypts the text using the key"""
    if p or q:
        return pow(m, e, p*q)
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
    val = generate_key()
    if val == None:
        print("Could not determine p, q, or d in a reasonable time - please use smaller numbers if you want to crack")
        exit()
    [p, q, d] = val
    print("p:", p)
    print("q:", q)
    print("d:", d)
    
    e = utils.modInverse(d, (p-1)*(q-1))
    
    # Encrypt a message
    m = 1234
    print("message:", m)
    c = encrypt(m, p*q, e)
    print("Cipher text:", c)
    
    # Decrypt a message
    print("Decrypted:", decrypt(c, p*q, d))
    
    # Crack a message
    print("Cracked:", crack(c, p*q, e))
    
