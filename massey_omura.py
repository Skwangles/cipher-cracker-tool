import utils

def encrypt(m, a, b, p):
    """Simulates the first 3 steps of the Massey-Omura protocol - A (sender) and B (receiver) transmitting a message m"""
    print("Simulating Massey-Omura...")

    # Step 0 - A and B calculates their own inverses (kept private)
    a_inv = utils.modInverse(a, p-1) 
    # b_inv = ... B's inverse is not needed for this 'encryption' function
    
    y1 = calculate_y1(m, a, p)
    print("y1 (A -> B):", y1)
    
    y2 = calculate_y2(y1, b, p)
    print("y2 (A <- B):", y2)
    
    y3 = calculate_y3(y2, a_inv, p)
    print("y3 (A -> B):", y3)

    print("Note: Receiver can now decrypt the following message using his inverse")
    return y3


def decrypt(m_b, b, p, b_inv=-1):
    """Decrypts m^b mod p using the receiver's private key to calculate the inverse and generate the key - p-1 is used as the modulus"""
    
    print("Receiver calculates his inverse...")
    if b_inv == -1:
        b_inv = utils.modInverse(b, p-1)
    
    print("Decrypting m...")
    return calculate_m_from_y3(m_b, b_inv, p)


def crack(m_a, m_ab, m_b, p):
    """Cracks the message m, and A & B's private keys"""
    
    # Uses a brute force method to find the key ('discrete logarithm problem')
    b_mod_p = find_key(m_a, m_ab, p)
    a_mod_p = find_key(m_b, m_ab, p)
    
    if a_mod_p == -1 or b_mod_p == -1:
        return "Could not determine a or b"

    print("A key:", a_mod_p)
    print("B key:", b_mod_p)
    
    # Decrypt the message using the cracked B
    print("Cracked message:") 
    return decrypt(m_b, b_mod_p, p)

def calculate_y1(m, a, p):
    """Calculates y1 (A -> B) - A sends m^a mod p to B"""
    return pow(m, a, p)

def calculate_y2(y1, b, p):
    """Calculates y2 (A <- B) - B sends y1^b mod p to A (which is now m^ab mod p)"""
    return pow(y1, b, p)

def calculate_y3(y2, a_inv, p):
    """Calculates y3 (A -> B) - A sends y2^(a^-1) mod p to B (which is now m^b mod p) and can be decrypted by B's inverse"""
    return pow(y2, a_inv, p)

def calculate_m_from_y3(y3, b_inv, p):
    """Calculates m (A <- B) - B decrypts y3 using his private key's inverse"""
    return pow(y3, b_inv, p)


def find_key(m_a, m_ab, p):
    """Brute forces the discrete logarithm problem to find the key"""
    if m_a == m_ab:
        return 1

    # Check powers 1 to p-1
    for i in range(1, p):
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
