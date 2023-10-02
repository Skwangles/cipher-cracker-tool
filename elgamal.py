import utils

def encrypt(m, yb, a, p, k=-1):
    """Encrypts the text using the key"""
    m = int(m)
    yb = int(yb)
    a = int(a)
    p = int(p)
    
    # k is random number between 1 and p-1
    if k == -1:
        k = utils.get_random_number(1, p-1)
    K = pow(yb, k, p)
    
    return [pow(a, k, p), (m * K) % p]


def decrypt(c1, c2, x, a, p):
    """Decrypts the cypher text using the y of Bob"""
    c1 = int(c1)
    c2 = int(c2)
    x = int(x)
    a = int(a)
    p = int(p)
    
    # get K from a^kx mod p
    K = pow(c1, x, p)
    K_inv = utils.modInverse(K, p)
    
    # Get m from Km mod p
    return (c2 * K_inv) % p


def crack(c1, c2,  yb, a, p, must_crack_b=False):
    """Cracks the cypher text, returning the key and message"""
    c1 = int(c1)
    c2 = int(c2)
    yb = int(yb)
    a = int(a)
    p = int(p)
    
    for i in range(1, p):
        val = pow(a, i, p)
        if val == c1 and not must_crack_b:
            K = pow(yb, i, p)
            K_inv = utils.modInverse(K, p)
            print("- Cracked k: ", i)
            return (c2 * K_inv) % p
        elif val == yb:
            # found Bob's private key
            print("- Found Receiver's private key: ", i)
            return decrypt(c1, c2, i, a, p)
        
    print("Couldn't find k or receiver's private key")
    return None
    
    
        
    


if __name__ == "__main__":
    
    print("El Gamal")
    print("--------")
    
    m = 7
    a = 5
    k = 3
    p = 23
    b = 6
    yb = 8
    
    
    # Q21 ii-iii) Numbers gained from the Assignment 2 question
    # m = 17
    # a = 5
    # k = 2
    # p = 23
    
    # b = 6
    # yb = pow(a, b, p)
    
    print("Encrypting message: ", m)
    print("Bob's public key: ", yb)
    print("Shared prime: ", a)
    print("Modulus: ", p)
    print("Random number: ", k)
    
    result = encrypt(m, yb, a, p, k)
    print("Encrypted message: ", result)
    print("Decrypting message: ", decrypt(int(result[0]), int(result[1]), b, a, p))
    
    print("Cracking message (most efficient): ", crack(2, 7, yb, a, p))    
    print("Cracking message (force b): ", crack(2, 7, yb, a, p, must_crack_b=True))  