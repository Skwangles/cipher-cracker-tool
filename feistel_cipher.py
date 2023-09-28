from math import ceil
import random
from alive_progress import alive_bar
import re
from utils import *
import hashlib
import itertools
ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"

def generate_combinations(max_length):
    for length in range(1, max_length + 1):
        for combo in itertools.product(ALPHABET, repeat=length):
            yield ''.join(combo)

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
    print("Cracking the cypher text... If your key is longer than 5 characters this will take a while...")
    MAX_KEY_CRACK_LENGTH = 10
    MAX_ROUNDS = 16
    initial_conversion = str(binary_to_string(cypher_text))
    if initial_conversion.isalnum() and index_of_coincidence(initial_conversion) > 0.066:
        print("No key needed - text is already decrypted")
        return binary_to_string(cypher_text)
    
    with alive_bar(pow(len(ALPHABET), MAX_KEY_CRACK_LENGTH) * MAX_ROUNDS) as bar:
        for i in range(MAX_ROUNDS, 1, -1):
                for key in generate_combinations(MAX_KEY_CRACK_LENGTH):
                    decrypted = str(decrypt(cypher_text, key, i))
                    # print("Trying key: " + key + " with " + str(i) + " rounds: " + decrypted[:20] + "...")
                    if decrypted.isalnum() and index_of_coincidence(decrypted) > 0.066:
                        # Finish the loading bars
                        bar(skipped=True)
                        print("Done")
                        return "Key: " + key + ", Plain Text: " + str(decrypt(cypher_text, key, i))
                    bar()
    return "No key found in the reasonable limits we've set - increase MAX_KEY_CRACK_LENGTH or MAX_ROUNDS"



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