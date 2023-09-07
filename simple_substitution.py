import random
import string

def encrypt(text, key):
    
    if len(key) != 26:
        return "Key is not long enough, one will be generated for you."
        key = generate_key()
   

    #Encrypt original text
    encrypted_text = []
    for char in text:
        if char.isalpha():
            if char.isupper():
                # Convert uppercase character to lowercase, substitute, then convert back to uppercase
                encrypted_text.append(key[char.lower()].upper())
            else:
                encrypted_text.append(key[char])
        else:
            encrypted_text.append(char)
    
    return ''.join(encrypted_text)



def decrypt(cypher_text, key):
    """Decrypts the cypher text using the key"""
    return "Not implemented"

def crack(cypher_text):
    """Cracks the cypher text, returning the key"""
    return "Not implemented"




#Generate key if one is not supplied
def generate_key():
    alphabet = list(string.ascii_lowercase)
    shuffled = random.sample(alphabet, len(alphabet))
    return dict(zip(alphabet, shuffled))
