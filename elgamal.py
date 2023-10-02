import utils

def encrypt(m, yb, a, p, k=-1):
    """Encrypts the text using the key"""
    
    # k is random number between 1 and p-1
    if k == -1:
        k = utils.get_random_number(1, p-1)
    K = pow(yb, k, p)
    
    return [pow(a, k, p), (m * K) % p]


def decrypt(c1, c2, x, a, p):
    """Decrypts the cypher text using the y of Bob"""
    
    # get K from a^kx mod p
    K = pow(c1, x, p)
    K_inv = utils.modInverse(K, p)
    
    # Get m from Km mod p
    return (c2 * K_inv) % p


def crack(c1, c2, ya, yb, a, p, must_crack_b=False):
    """Cracks the cypher text, returning the key and message"""
    crackedB = False
    k = -1
    for i in range(1, p):
        val = pow(a, i, p)
        if val == c1 and not must_crack_b:
            # found little k
            k = i
            break
        elif val == yb:
            # found Bob's private key
            k = i
            crackedB = True
            break
        
    if k == -1:
        print("Couldn't " + ("find k or " if not must_crack_b else "") +"receiver's private key")
        return "No key found"
    
    if crackedB:
        print("Cracked receiver's private key: ", k)
        return decrypt(c1, c2, k, a, p)
    
    K = pow(yb, k, p)
    K_inv = utils.modInverse(K, p)
    print("Cracked k: ", k)
    return (c2 * K_inv) % p
        
    


if __name__ == "__main__":
    
    print("El Gamal")
    print("--------")
    m = 7
    ya = 4
    yb = 8
    a = 3
    k=3
    p = 17
    print("Encrypting message: ", m)
    print("Bob's public key: ", yb)
    result = encrypt(m, yb, a, p, k)
    print("Encrypted message: ", result)
    print("Decrypting message: ", decrypt(int(result[0]), int(result[1]), ya, a, p))
    print("Cracking message: ", crack(int(result[0]), int(result[1]), ya, yb, a, p))    