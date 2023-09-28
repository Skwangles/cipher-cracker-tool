import utils

def encrypt(m, a, b, p):
    """Encrypts the text using the key"""
    # Get the inverse of a and b - private information
    a_inv = utils.get_modular_inv(a, p) 
    b_inv = utils.get_modular_inv(b, p) 
    if a_inv == -1 or b_inv == -1:
        return "No inverse found"
    
    # Calculate the cipher text
    m_a = pow(m, a) % p
    
    # Bob sends m_ab to Alice
    m_ab = agree_on_key(m_a, b, p)
    
    # Alice sends m_b to Bob - this is the cipher text, and can be decrypted by Bob's private key b
    m_b = pow(m_ab, a_inv) % p

    print("m^a:", m_a)
    print("m^ab:", m_ab)
    print("p:", p)
    print("Cipher Text to bob:")
    return m_b


def decrypt(m_b, b, p, b_inv=-1):
    """Decrypts the cypher text using the m^b"""
    if b_inv == -1:
        b_inv = utils.get_modular_inv(b, p)
        
    return pow(m_b, b_inv) % p


def crack(m_a, m_ab, m_b, p):
    """Cracks the cypher text, returning the key"""
    b_mod_p = find_key(m_a, m_ab, p)
    a_mod_p = find_key(m_b, m_ab, p)
    if a_mod_p == -1 or b_mod_p == -1:
        return "Could not determine a or b (e.g. m^a mod p) in a reasonable time - please use smaller numbers if you want to crack"

    print("alice key:", a_mod_p)
    print("bob key:", b_mod_p)

    return pow(m_b, b_mod_p) % p


def agree_on_key(base, exp, p):
    """Agrees on a value"""
    return pow(base, exp) % p


def find_key(m_a, m_ab, p):
    """Gets the power """
    if m_a == m_ab:
        return 1
    
    for i in range(2, p):
        if (pow(m_a, i) % p) == m_ab:
            return i
    return -1

if __name__ == "__main__":
    print("Running Massey-Omura")
    print("Encrypting 5 with a=3, b=7, p=11")
    result = encrypt(5, 3, 7, 11)
    print(result)
   
    print("Decrypting result")
    print(decrypt(11, b=b, p=p))
    print("Cracking")
    print(crack(7, 12, 11, 17))