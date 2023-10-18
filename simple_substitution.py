import random
import string
from alive_progress import alive_bar
from utils import *
import re

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ABSOLUTE_MINIMUM = int(-1e99)

#Generate key if one is not supplied
def generate_key():
    alphabet = list(string.ascii_lowercase)
    shuffled = random.sample(alphabet, len(alphabet))
    return dict(zip(alphabet, shuffled))


def get_english_frequencies():
    # Approximate frequency of letters in the English language.
    # You can adjust these values based on more detailed studies.
    return {
        'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
        'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
        'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
        'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
        'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 'Z': 0.00074
    }
    

def encrypt(text, key):
    """Encrypt the plain text using the key"""
    if not text:
        return "Missing required arguments for this function"
    
    alphabet = get_alphabet()
    
    text = text.upper()
    key = key.upper()

    # Validate the key
    if len(key) != 26 or len(set(key)) != 26:
        raise ValueError("Key must be a permutation of the English alphabet")

    encrypted_text = ""
    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            encrypted_text += key[index]
        else:
            encrypted_text += char

    return encrypted_text


def decrypt(cypher_text, key):
    """Decrypts the cypher text using the key"""
    if not cypher_text:
        return "Missing required arguments for this function"
    
    alphabet = get_alphabet()
    
    cypher_text = cypher_text.upper()
    key = key.upper()

    # Validate the key
    if len(key) != 26 or len(set(key)) != 26:
        raise ValueError("Key must be a permutation of the English alphabet")

    decrypted_text = ""
    for char in cypher_text:
        if char in key:
            index = key.index(char)
            decrypted_text += alphabet[index]
        else:
            decrypted_text += char

    decrypted_text = decrypted_text.lower()

    return decrypted_text


def crack(cypher_text):
    """Cracks the cypher text, returning the key"""       
    if not cypher_text:
        return "Missing required arguments for this function"    
    
    # Remove non-alphabetic characters, cracking only uses letters
    cypher_text = cypher_text.upper()
    cypher_text = re.sub(r'[^A-Z\s]', '', cypher_text)
    
    frequencies = get_english_frequencies()
    cipher_frequencies = {char: cypher_text.count(char) / len(cypher_text) for char in ALPHABET}
    
    # Frequency analysis letters to build a starting point for the mapping
    sorted_english = sorted(frequencies.keys(), key=lambda x: frequencies[x], reverse=True)
    sorted_cipher = sorted(cipher_frequencies.keys(), key=lambda x: cipher_frequencies[x], reverse=True)
    
    # Create a mapping between the cipher letter and the estimated English letter
    mapping = get_empty()
    for cipher_letter, english_letter in zip(sorted_cipher, sorted_english):
        mapping[cipher_letter] = english_letter

    # Randomly swap letters in the mapping, gradually improving the 'fitness' of the mapping
    hill_climbed_map = hill_climb(mapping, cypher_text)    

    print("Key:", mapping_to_key(hill_climbed_map))
    return apply_mapping_to_text(cypher_text, hill_climbed_map)


### Formatting/Utils ###

def apply_mapping_to_text(cypher_text, mapping, separator="*"): 
    """Returns the cypher text with the mapping applied"""
    decrypted = ""
    for letter in cypher_text:
        if letter.upper() in mapping:
            if mapping[letter.upper()] is None:
                decrypted += separator
            else:
                decrypted += mapping[letter.upper()]
        else:
            decrypted += letter

    return decrypted


def mapping_to_key(mapping):
    """Returns key string based on alphabetical order of 'values' of the mappings"""
    keys = sorted(mapping.items(), key=lambda x: x[1])
    return "".join(key[0] for key in keys)   


def get_empty():
    """Returns an empty mapping - with all letters of the alphabet"""
    return {
        'A': None,
        'B': None,
        'C': None,
        'D': None,
        'E': None,
        'F': None,
        'G': None,
        'H': None,
        'I': None,
        'J': None,
        'K': None,
        'L': None,
        'M': None,
        'N': None,
        'O': None,
        'P': None,
        'Q': None,
        'R': None,
        'S': None,
        'T': None,
        'U': None,
        'V': None,
        'W': None,
        'X': None,
        'Y': None,
        'Z': None
        }    

### Hill Climb to find local maxima ###

def hill_climb(mapping, cypher_text):
    best = mapping
    best_fitness = get_english_score(apply_mapping_to_text(cypher_text, best))
    with alive_bar(2500) as bar:
        # Hill climb for 1000 iterations
        for i in range(2500):
            new_map = swap_randomly(best.copy())
            new_percent = get_english_score(apply_mapping_to_text(cypher_text, new_map))
            if new_percent > best_fitness:
                best = new_map
                best_fitness = new_percent
            bar()
    return best

def swap_randomly(mapping):
    key1 = random.randrange(0, len(ALPHABET))
    key2 = random.randrange(0, len(ALPHABET))
    while key1 == key2:
        key2 = random.randrange(0, len(ALPHABET))
    
    temp = mapping[ALPHABET[key1]]
    mapping[ALPHABET[key1]] = mapping[ALPHABET[key2]]
    mapping[ALPHABET[key2]] = temp
    return mapping

if __name__ == "__main__":
    text = """The cab arrived late. The inside was in as bad of shape as the outside which was concerning, and it didn't appear that it had been cleaned in months. The green tree air-freshener hanging from the rearview mirror was either exhausted of its scent or not strong enough to overcome the other odors emitting from the cab. The correct decision, in this case, was to get the hell out of it and to call another cab, but she was late and didn't have a choice.
    
    She closed her eyes and then opened them again. What she was seeing just didn't make sense. She shook her head seeing if that would help. It didn't. Although it seemed beyond reality, there was no denying she was witnessing a large formation of alien spaceships filling the sky.
    
    He watched as the young man tried to impress everyone in the room with his intelligence. There was no doubt that he was smart. The fact that he was more intelligent than anyone else in the room could have been easily deduced, but nobody was really paying any attention due to the fact that it was also obvious that the young man only cared about his intelligence.
    """
    key = generate_key()
    key = "".join(key[letter] for letter in key)
    print("Key:", key)
    encrypted = encrypt(text, key)
    print("Encrypted:", encrypted)
    decrypted = decrypt(encrypted, key)
    print("Decrypted:", decrypted)
    cracked = crack(encrypted)
    print("Cracked:", cracked)
    print("Original:", get_english_score(text))
    print("Cracked:", get_english_score(cracked))
    print("Actual Key:", key.upper())   