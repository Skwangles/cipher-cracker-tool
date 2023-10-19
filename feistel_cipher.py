from math import ceil
import random
from alive_progress import alive_bar
import re
from string_conversions import *
from utils import *
import hashlib
ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"

def get_sub_key(key, round, block_size=16):
    """Generates subkey through a relationship with the main key"""
    # Hash the main key - append the  'round #' to change the result
    hashed_key = string_to_binary(str(hashlib.sha256((key + "_" + str(round)).encode()).hexdigest()))
    
    # Repeat hash if too short for the feistel network's L half
    if len(hashed_key) < block_size:
        hashed_key = hashed_key + hashed_key * (block_size // len(hashed_key))
        return hashed_key[:block_size]

    return hashed_key[:block_size]
 

def encrypt(text, key="", rounds=16):
    """Encrypts the text using the key - calling the feistel network x rounds"""
  
    if not key or len(key) == 0:
        return "No key provided"   
    
    print("Removing all non-alphanumeric characters from text")
    text = re.sub("[^a-zA-Z0-9\\s]+", "", text)
    
    # binary is used for the feistel cipher, so convert to binary
    binary_string = string_to_binary(text)
    
    # sanity check - should never happen
    if len(binary_string) % 2 != 0: 
        print("Text is not a multiple of 2, padding with a 0")
        binary_string += "0"

    L = binary_string[:len(binary_string)//2]
    R = binary_string[len(binary_string)//2:]


    return binary_to_hex(str(feistel_cipher(L, R, key=key, rounds=rounds)))


def decrypt(cypher_text, key="", rounds=16):
    """Decrypts the cypher text using the key - cypher text must be a hex string"""
    
    if re.match("^[a-f0-9A-F]+$", cypher_text) is None:
        raise Exception("Cypher text is not a binary string")
    
    if not key or len(key) == 0:
            return "No key(s) provided, or keys are not a multiple of keylength"        
    
    # binary is used for the feistel cipher, so convert to binary
    cypher_text = hex_to_binary(str(cypher_text))
    
    # feistel network has two even halves as input - so split binary string in half
    L= cypher_text[:len(cypher_text)//2]
    R= cypher_text[len(cypher_text)//2:]
    
    return binary_to_string(feistel_cipher(L, 
                         R, key=key,
                          rounds=rounds, reversed=True))


def feistel_cipher(L, R, key, rounds=16, reversed=False):
    """Feistel cipher - encrypts the text using the key - input/output are binary strings"""

    Li_less_1 = L
    Ri_less_1 = R

    for i in range(0, rounds):        
        # Apply f function to right half and key
        position = i
        if reversed:
            position = (rounds-1) - i 
            
        # using the key generate a sub-key to then obscure the right half
        pre_xor_Ri = f_func(Ri_less_1, get_sub_key(str(key), position, block_size=len(Ri_less_1)))

        # XOR the output of the f function with the left half
        Ri = xor_string_and_key(Li_less_1, pre_xor_Ri)
        
        # Old right half becomes left half unchanged
        Li = Ri_less_1

        # Pass output to next round
        Li_less_1 = Li
        Ri_less_1 = Ri

    # Final step is to join the two halves, flipping them in the process
    return str(Ri_less_1) + str(Li_less_1)


def f_func(text, key):
    """The f function used in the Feistal cipher - xor text with sub-key"""
    return xor_string_and_key(text, key)


if __name__ == "__main__":
    print("Feistel cipher")
    print("--------------")
    
    print("Encrypting 'Hello World' with key 'key' and 16 rounds")
    key = "hel"
    cypher_text = encrypt(text="im not going to encrypt anything", key=key, rounds=16)
    print(cypher_text)
    print("------------------")
    print("Decrypting with key")
    print(decrypt(cypher_text, key, 16))
    