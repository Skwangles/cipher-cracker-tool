import random
import math
import utils
import sympy
import threading
from alive_progress import alive_bar

RSA_PRIME_MAX = 100_000_000_000_000_000_000
RSA_PRIME_MIN = 100_000_000_000_000

def generate_weak_key(min=RSA_PRIME_MIN, max=RSA_PRIME_MAX):
    p = sympy.randprime(min, max)
    q = sympy.nextprime(sympy.nextprime(p))
    while p == q:
        q = sympy.randprime(min, max)
    
    fi_n = (p-1)*(q-1)
    
    e = 11 # small enough so that m^e is < n  - ideally 65537
    if e > fi_n:
        print("fi_n is too small for default e, generating a new e")
        e = sympy.randprime(2, fi_n)
        
    
    d = utils.modInverse(e, fi_n)

    print("e:", e)
    print("n:", p*q)
    
    return [p, q, d]

def FermatFactors(n):
    
    
    # if n%2 ==0 then return the factors
    if n % 2 == 0:
        return str(n // 2) + ", 2"
     
    # find the square root
    a = math.ceil(math.sqrt(n))
     
    # if the number is a perfect square
    if a * a == n:
        return [a, a]
     
    # else perform factorisation
    while True:
        b1 = a * a - n
        
        b = math.floor(math.sqrt(b1))
         
        if b * b == b1:
            break
        else:
            a += 1
     
    return [int(a - b), int(a + b)]
        
    


def find_p_q_d(n, e):
    """Finds p, q, and d given n and e"""
    
    p = 0
    q = 0
    d = 0

    #fermats_thread = threading.Thread(target=fermats_factorisation, args=(n,))

    [p, q] = FermatFactors(int(n))
            
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
    m = 1234
    print("message:", m)
    c = encrypt(m, p*q, e)
    print("Cipher text:", c)
    
    # Decrypt a message
    print("Decrypted:", decrypt(c, p*q, d))
    
    # Crack a message
    print("Cracked:", crack(c, p*q, e))
    
