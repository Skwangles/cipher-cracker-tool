from math import ceil
import random
import re
from utils import *
import hashlib

def get_sub_key(key, round, block_size=16):
    """Generates subkey through a relationship with the main key"""
    # Hash the main key - add 'round' to change the result
    hashed_key = string_to_binary(str(hashlib.sha256((key + "_" + str(round)).encode()).hexdigest()))
    
    # Case hash is too small
    if len(hashed_key) < block_size:
        hashed_key = hashed_key + hashed_key * (block_size // len(hashed_key))
        return hashed_key[:block_size]

    return hashed_key[:block_size]
 

def encrypt(text, key="", rounds=16):
    """Encrypts the text using the key"""
    rounds = int(rounds)
    key = str(key)
    rounds = int(rounds)
  
    if not key or len(key) == 0:
        return "No key(s) provided"        
    
    text = string_to_binary(text)
    
    # sanity check - should never happen
    if len(text) % 2 != 0: 
        print("Text is not a multiple of 2, padding with a 0")
        text += "0"

    L = text[:len(text)//2]
    R = text[len(text)//2:]
    
    return str(feistel_cipher(L, R, key=key, rounds=rounds))


def decrypt(cypher_text, key="", rounds=16):
    """Decrypts the cypher text using the key - cypher text must be a binary string"""
    rounds = int(rounds)
    key = str(key)
    
    if re.match("^[01]+$", cypher_text) is None:
        return "Cypher text is not a binary string"
    
    if not key or len(key) == 0:
            return "No key(s) provided, or keys are not a multiple of keylength"        
    
    #Text is already a binary string, so no need to convert
    
    return binary_to_string(feistel_cipher(cypher_text[:len(cypher_text)//2], 
                          cypher_text[len(cypher_text)//2:], key=key,
                          rounds=rounds, reversed=True))


def feistel_cipher(L, R, key, rounds=16, reversed=False):
    """Feistel cipher - encrypts the text using the key"""

    Li_less_1 = L
    Ri_less_1 = R

    for i in range(0, rounds):        
        # Apply f function to right half and key
        position = i
        if reversed:
            position = (rounds-1) - i 
        pre_xor_Ri = f_func(Ri_less_1, get_sub_key(key, position))

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
    return xor_string_and_key(text, key)

def crack(cypher_text):
    """Cracks the cypher text, returning the key"""    
    return "Sorry bucko, you're on your own - this would take way too long to crack during this presentation"

if __name__ == "__main__":
    print("Feistel cipher")
    print("--------------")
    
    print("Encrypting 'Hello World' with key 'key' and 16 rounds")
    cypher_text = encrypt("imnotencryptinganything", "asuperlongkeyisnowused", 16)
    print(cypher_text)
    print("------------------")
    print("Decrypting 'Hello World' with key 'keyasdfs' and 16 rounds")
    print(decrypt(cypher_text, "asuperlongkeyisnowused", 16))
    
    print("Cracking 'Hello World'")
    print(crack(cypher_text))