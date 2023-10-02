import utils

def encrypt(m, a, b, p):
    """Encrypts the text using the key"""
    # Get the inverse of a and b - private information
    a_inv = utils.modInverse(a, p-1) 
    b_inv = utils.modInverse(b, p-1) 
    
    # Step 1 - Alice sends m to Bob
    m_a = pow(m, a, p)
    
    # Step 2 - Alice sends m_a to Bob
    m_ab = pow(m_a, b, p)
    
    # Step 4 - Alice multiplies by her inverse to get m_b
    m_b = pow(m_ab, a_inv, p)
    

    print("y1:", m_a)
    print("y2:", m_ab)
    print("p:", p)
    print("Cipher Text to bob (y3):")
    return m_b


def decrypt(m_b, b, p, b_inv=-1):
    """Decrypts the cypher text using the m^b"""
    if b_inv == -1:
        b_inv = utils.modInverse(b, p-1)
        
    return pow(m_b, b_inv, p)


def crack(m_a, m_ab, m_b, p):
    """Cracks the cypher text, returning the key"""
    b_mod_p = find_key(m_a, m_ab, p)
    a_mod_p = find_key(m_b, m_ab, p)
    if a_mod_p == -1 or b_mod_p == -1:
        return "Could not determine a or b (e.g. m^a mod p) in a reasonable time - please use smaller numbers if you want to crack"

    print("A key:", a_mod_p)
    print("B key:", b_mod_p)

    return pow(m_b, b_mod_p) % p


def find_key(m_a, m_ab, p):
    """Gets the power """
    if m_a == m_ab:
        return 1
    
    for i in range(2, p):
        if (pow(m_a, i, p)) == m_ab:
            return i
    return -1

if __name__ == "__main__":
    
    print("Running Massey-Omura")
    
    # Worked example
    # step 1 - ma = 7
    # step 2 - mab = 12
    # step 3 - mb = 11
    # step 4 - m = 3
    
    m = 3
    a = 11
    b = 7
    p = 17
    
    print("### Encrypting: ", m, "###")
    result = encrypt(m=m, a=a, b=b, p=p)
    print(result)
   
    print("### Decrypting result ###")
    print(decrypt(result, b=b, p=p))
    
    print("### Cracking ###")
    print(crack(7, 12, 11, 17))