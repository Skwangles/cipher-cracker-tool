import random
import string
from alive_progress import alive_bar
from utils import *
from nltk.corpus import words 
import re
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
FREQUENCY_ALPHABET = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

english_words = None

if not english_words:
    try:
        nltk.data.find('corpora/words.zip')
    except LookupError:
        nltk.download('words')

    english_words = set(words.words())

word_patterns = {}


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


def crack(cypher_text):
    """Cracks the cypher text, returning the key"""       
    if not cypher_text:
        return "Missing required arguments for this function"    
    
    # Frequency order
    english_freq_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    mapping = get_empty()
    
    
    cypher_text = cypher_text.upper()
    cypher_text = re.sub(r'[^A-Z\s]', '', cypher_text)
    
    
    # first pass - find words that could match each 'word' in the cypher text
    encrypted_words = cypher_text.split(" ")
    
    # check longest words first as they have the most information
    encrypted_words = sorted(encrypted_words, key=len, reverse=True)
    
    
    with alive_bar(len(encrypted_words)) as bar:
        for c_word in encrypted_words:
            pattern = get_pattern_of_unique(c_word)
            
            if pattern not in word_patterns:
                continue
            
            single_word_map = get_empty()
            for possible_word in word_patterns[pattern]:
                for i in range(len(c_word)):
                    if c_word[i] in single_word_map:
                        letter = possible_word[i]
                        if letter not in single_word_map[c_word[i]]:
                            single_word_map[c_word[i]].append(letter)
            bar()
            mapping = addGuessesToMap(mapping, single_word_map)
    
    mapping = collapse_solved_letters(mapping)
    print(mapping)
    
    local_maxima = hill_climb_blank(hill_climb_undecided(mapping, cypher_text), cypher_text)

    print("Key:", mapping_to_key(local_maxima))
    return apply_mapping_to_text(cypher_text, local_maxima)

### Formatting/Utils ###

def get_missing_letters(mapping):
    present_letters = set()
    for key in mapping:
        if len(mapping[key]) != 0:
            for letter in mapping[key]:
                present_letters.add(letter)
                
    missing_letters = []
    for letter in ALPHABET:
        if letter not in present_letters:
            missing_letters.append(letter)
    return missing_letters


def mapping_to_key(mapping):
    
    keys = sorted(mapping.items(), key=lambda x: x[1])
    return "".join(key[0] for key in keys)
        

def get_empty():
    
    return {
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

def count_of_items_with_1(mapping):
    count = 0
    for key in mapping:
        if len(mapping[key]) == 1:
            count += 1
    return count


def collapse_solved_letters(mapping):
    unsolved_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    with alive_bar(len(unsolved_letters)) as bar:
        while unsolved_letters and any(len(mapping[letter]) == 1 for letter in unsolved_letters):
            letters_with_1 = [letter for letter in unsolved_letters if len(mapping[letter]) == 1]
            
            # order by highest frequency - i.e. choose 1st preference of the most common letters first
            letters_with_1.sort(key=lambda x: FREQUENCY_ALPHABET.find(x))
            print(letters_with_1)
            
            for letter in letters_with_1:
                if len(mapping[letter]) != 1:
                    continue
                
                bar()
                
                solved_letter = mapping[letter][0]
                
                unsolved_letters = unsolved_letters.replace(letter, "")
                
                # remove solved letter from all other mappings
                for key in unsolved_letters:
                    if key == letter:
                        continue
                    
                    if solved_letter in mapping[key]:
                        mapping[key].remove(solved_letter) 
    return mapping
            
 
def addGuessesToMap(root_map, single_map):
    """Reduces the root_map to only contain letters that are in both root_map and single_map"""
    intersection = get_empty()
    for key in root_map:
        if key not in single_map:
            intersection[key] = root_map[key]
            continue
        
        for letter in root_map[key]:
            if letter in single_map[key]:
                intersection[key].append(letter)
        
        if len(intersection[key]) == 0:
            # root_map and single_map have no letters in common - join them
            intersection[key] = root_map[key] + single_map[key]
        
    return intersection

EARLY_EXIT = 80 # accept 80% to avoid falling into brute force

def hill_climb_undecided(mapping, cypher_text):
    non_empty = filter(lambda x: len(x[1]) > 1, mapping.items())
    non_solved = sorted(non_empty, key=lambda x: len(x[1]))
    
    if len(non_solved) == 0:
        return mapping
    
    letter, possible = non_solved[0]
    
    print("Hill climbing", letter, "with", len(possible), "possibilities")
    best_match = None
    best_match_percent = -1

    for guess in possible:
        print("Guessing", letter, "is", guess)
        new_mapping = collapse_solved_letters(addGuessesToMap(mapping, {letter: [guess]}))
        decrypted = apply_mapping_to_text(cypher_text, new_mapping)
        percent = get_english_percent(decrypted)
        print(percent)
        if percent > best_match_percent:
            best_match = new_mapping
            best_match_percent = percent
            if percent > EARLY_EXIT:
                print("Early exit")
                return best_match
                
    if best_match_percent == -1:
        print("No matches found")
        return mapping
    return hill_climb_undecided(best_match, cypher_text)

def hill_climb_blank(mapping, cypher_text):
    if any(len(mapping[letter]) > 1 for letter in mapping):
        print("You must have completely 'solved' all letters before running this!")
        raise ValueError("Must completely solve before filling blanks")
    
    unassigned = get_missing_letters(mapping)
    empty_spots = list(filter(lambda x: len(x[1]) == 0, mapping.items()))
    
    best_match = None
    best_match_percent = -1
    
    if len(empty_spots) == 0:
        return mapping
    
    letter, _ = empty_spots[0]
    print("Hill climbing", letter, "with", len(unassigned), "possibilities")
    
    for guess in unassigned:
        new_mapping = collapse_solved_letters(addGuessesToMap(mapping, {letter: [guess]}))
        decrypted = apply_mapping_to_text(cypher_text, new_mapping)
        percent = get_english_percent(decrypted)
        print(percent)
        if percent > best_match_percent:
            best_match = new_mapping
            best_match_percent = percent
            if percent > EARLY_EXIT:
                print("Early exit")
                return best_match
                
    if best_match_percent == -1:
        print("No matches found")
        return mapping
    
    return hill_climb_blank(best_match, cypher_text)
    

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

def apply_mapping_to_text(cypher_text, mapping): 
    decrypted = ""
    for letter in cypher_text:
        if letter.upper() in mapping:
            if len(mapping[letter.upper()]) > 1 or len(mapping[letter.upper()]) == 0:
                decrypted += "*"
            else:
                decrypted += mapping[letter.upper()][0]
        else:
            decrypted += letter

    return decrypted

# store the set of words and what they look like globally so we dont have to spend ages getting them each time
for word in english_words:
    pattern = get_pattern_of_unique(word)
    if pattern not in word_patterns:
        word_patterns[pattern] = [word.upper()]
    else:
        word_patterns[pattern].append(word.upper())


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
    print("Cracked %:", get_english_percent(cracked))
    print("Actual Key:", key.upper())   