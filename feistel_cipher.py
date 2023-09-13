import random
import re
from utils import *


def encrypt(text, keys="", keylength=3, rounds=16):
    """Encrypts the text using the key"""
    keylength = int(keylength)
    rounds = int(rounds)
    keys = str(keys)
    
    if len(text) % 2 != 0:
        print("Text is not a multiple of 2, padding with 1x# at the end")
        text = text + "#" # Pad to a multiple of 2
    
    if not keys or len(keys) == 0 or len(keys) % keylength != 0:
            return "No key(s) provided, or keys are not a multiple of keylength"        
    
    keyspace = [keys[i:i+keylength] for i in range(0, len(keys), keylength)]
    
    text = string_to_binary(text)

    L = text[:len(text)//2]
    R = text[len(text)//2:]
    
    return str(feistel_cipher(L, R, rounds=rounds, keyspace=keyspace))


def decrypt(cypher_text, keys="", keylength=3, rounds=16):
    """Decrypts the cypher text using the key - cypher text must be a binary string"""
    keylength = int(keylength)
    rounds = int(rounds)
    keys = str(keys)
    
    if re.match("^[01]+$", cypher_text) is None:
        return "Cypher text is not a binary string"
    
    if not keys or len(keys) == 0 or len(keys) % keylength != 0:
            return "No key(s) provided, or keys are not a multiple of keylength"        
    
    keyspace = [keys[i:i+keylength] for i in range(0, len(keys), keylength)]

    # Decrypting is the same as encrypting, but with the keys in reverse order
    keyspace.reverse() 
    
    #Text is already a binary string, so no need to convert
    
    return binary_to_string(str(feistel_cipher(cypher_text[:len(cypher_text)//2], 
                          cypher_text[len(cypher_text)//2:], 
                          keyspace=keyspace,
                          rounds=rounds)))


def feistel_cipher(L, R, keyspace, rounds=16):
    """Feistel cipher - encrypts the text using the key"""

    Li_less_1 = L
    Ri_less_1 = R
    
    for i in range(rounds):
        key = keyspace[i % len(keyspace)]
        pre_xor_Ri = f_func(Ri_less_1, key)

        # XOR the output of the f function with the left half
        Ri = xor_string_and_key(Li_less_1, pre_xor_Ri)
        Li = Ri_less_1

        # Pass output to next round
        Li_less_1 = Li
        Ri_less_1 = Ri

    # Final step is to join the two halves, flipping them in the process
    return str(Ri_less_1) + str(Li_less_1)


def f_func(text, key):
    """The f function used in the Feistal cipher"""
    # Hash the text and key - doesn't need to be invertible
    return xor_string_and_key(text, string_to_binary(key))


def crack(cypher_text):
    """Cracks the cypher text, returning the key"""    
    return "Sorry bucko, you're on your own - this would take way too long to crack during this presentation"

if __name__ == "__main__":
    print("Feistel cipher")
    print("--------------")
    
    print("Encrypting 'Hello World' with key 'key' and 16 rounds")
    cypher_text = encrypt("Hello World", "key")
    print(cypher_text)
    
    print("Decrypting 'Hello World' with key 'key' and 16 rounds")
    print(decrypt(cypher_text, "key"))
    
    print("Cracking 'Hello World'")
    print(crack(cypher_text))