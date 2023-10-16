import random
import string

from utils import *
from nltk.corpus import words 

empty_mapping = {
 'A': [],
 'B': [],
 'C': [],
 'D': [],
 'E': [],
 'F': [],
 'G': [],
 'H': [],
 'I': [],
 'J': [],
 'K': [],
 'L': [],
 'M': [],
 'N': [],
 'O': [],
 'P': [],
 'Q': [],
 'R': [],
 'S': [],
 'T': [],
 'U': [],
 'V': [],
 'W': [],
 'X': [],
 'Y': [],
 'Z': []
}


english_words = None

if not english_words:
    try:
        nltk.data.find('corpora/words.zip')
    except LookupError:
        nltk.download('words')

    english_words = set(words.words())

word_patterns = {}


def get_pattern_of_unique(word):
    letters = {}
    output = ""
    num = 0
    separator = "|"
    for letter in word:
        if letter not in letters:
            num += 1
            letters[letter] = num
        output += separator + str(letters[letter]) # e.g. "1|2|3|4..."
    return output



#Generate key if one is not supplied
def generate_key():
    alphabet = list(string.ascii_lowercase)
    shuffled = random.sample(alphabet, len(alphabet))
    return dict(zip(alphabet, shuffled))


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

def dict_to_sorted_list(dict):
    """Converts a dictionary to a sorted list"""
    return sorted(dict.items(), key=lambda x: x[1], reverse=True)

def GetShortestEntry(list):
    """Sorts a list"""
    return sorted(list, key=lambda x: len(x[1]))[0]


def crack(cypher_text):
    """Cracks the cypher text, returning the key"""       
    if not cypher_text:
        return "Missing required arguments for this function"    
    
    # Frequency order
    english_freq_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    output_mapping = empty_mapping.copy()
    mapping = empty_mapping.copy()
    
    # first pass - find words that could match each 'word' in the cypher text
    encrypted_words = cypher_text.split(" ")
    
    # check longest words first as they have the most information
    encrypted_words = sorted(encrypted_words, key=len, reverse=True)
    
    for c_word in encrypted_words:
        pattern = get_pattern_of_unique(c_word)
        if pattern not in word_patterns:
            continue
                
        for possible_word in word_patterns[pattern]:
            for i in range(len(c_word)):
                if c_word[i] in mapping:
                    letter = possible_word[i]
                    if letter not in mapping[c_word[i]]:
                        mapping[c_word[i]].append(letter)

    sorted_mappings = sorted(mapping.items(), key=lambda x: len(x[1]))
    
    while any(len(x[1]) == 1 for x in sorted_mappings):
        least = GetShortestEntry(sorted_mappings)
        if len(least[1]) == 0:
            # we don't have have any more letters to assign to this mapping, so remove it
            sorted_mappings.remove(least)
            continue
        if len(least[1]) == 1:
            # we have found the letter for this mapping, so remove it from all other mappings
            sorted_mappings = remove_letter_from_mapping_dict(sorted_mappings, least[1][0], least[0])
            sorted_mappings.remove(least)
            continue
               

    print(output_mapping)

    decrypted = ""
    for letter in cypher_text:
        if letter.upper() in output_mapping:
            if letter.isupper():
                decrypted += output_mapping[letter.upper()][0]
            else:
                decrypted += output_mapping[letter.upper()][0].lower()
        else:
            decrypted += letter

    return decrypted


def remove_letter_from_mapping_dict(mapping, letter, current_letter):
    """Remove letter which has been assigned from all other 'potential' mappings"""
    for key in mapping:
        if key == current_letter:
            continue
        if letter in mapping[key]:
            mapping[key].remove(letter)
    return mapping


# store the set of words and what they look like globally so we dont have to spend ages getting them each time
for word in english_words:
    pattern = get_pattern_of_unique(word)
    if pattern not in word_patterns:
        word_patterns[pattern] = [word.upper()]
    else:
        word_patterns[pattern].append(word.upper())
        

if __name__ == "__main__":
    text = "This is a super long text string which I will use to test the functionality of the system is it made of various common words that i hope this system can pick our without any issues so please I hope it works this is the best way to check that this test works well the quick brown fox jumps over the lazy dog"
    key = generate_key()
    key = "".join(key[letter] for letter in key)
    print("Key:", key)
    encrypted = encrypt(text, key)
    print("Encrypted:", encrypted)
    decrypted = decrypt(encrypted, key)
    print("Decrypted:", decrypted)
    cracked = crack(encrypted)
    print("Cracked:", cracked)
    print("Cracked %:", get_english_percent(cracked))