import random
import string
from alive_progress import alive_bar
from utils import *
from nltk.corpus import words 
import re
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


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
    
    for c_word in encrypted_words:
        pattern = get_pattern_of_unique(c_word)
        
        if pattern not in word_patterns:
            continue
        
        if len(word_patterns[pattern]) == 1:
            # we have found the word, so add it to the mapping
            for i in range(len(c_word)):
                mapping[c_word[i]] = [word_patterns[pattern][0][i]]
            continue
        
        single_word_map = get_empty()
        with alive_bar(len(word_patterns[pattern])) as bar:
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
    
    return apply_mapping_to_text(cypher_text, mapping)


def collapse_solved_letters(mapping):
    unsolved_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    with alive_bar(len(unsolved_letters)) as bar:
        while unsolved_letters and any(len(mapping[letter]) == 1 for letter in unsolved_letters):
            letters_with_1 = [letter for letter in unsolved_letters if len(mapping[letter]) == 1]
            
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
    

def count_of_items_with_1(mapping):
    count = 0
    for key in mapping:
        if len(mapping[key]) == 1:
            count += 1
    return count
            
def check_if_any_match(mapping, letter, others_with_1):
    output = []
    for other in others_with_1:
        if letter in mapping[other]:
            output.append(other)
    return output
    
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





# store the set of words and what they look like globally so we dont have to spend ages getting them each time
for word in english_words:
    pattern = get_pattern_of_unique(word)
    if pattern not in word_patterns:
        word_patterns[pattern] = [word.upper()]
    else:
        word_patterns[pattern].append(word.upper())


if __name__ == "__main__":
    text = """Robert Frost was born in San Francisco, but his family moved to Lawrence, Massachusetts, in 1884 following his father’s death. The move was actually a return, for Frost’s ancestors were originally New Englanders, and Frost became famous for his poetry’s engagement with New England locales, identities, and themes. Frost graduated from Lawrence High School, in 1892, as class poet (he also shared the honor of co-valedictorian with his wife-to-be Elinor White), and two years later, the New York Independent accepted his poem entitled “My Butterfly,” launching his status as a professional poet with a check for $15.00. Frost's first book was published around the age of 40, but he would go on to win a record four Pulitzer Prizes and become the most famous poet of his time, before his death at the age of 88.
 
To celebrate his first publication, Frost had a book of six poems privately printed; two copies of Twilight were made—one for himself and one for his fiancee. Over the next eight years, however, he succeeded in having only 13 more poems published. During this time, Frost sporadically attended Dartmouth and Harvard and earned a living teaching school and, later, working a farm in Derry, New Hampshire. But in 1912, discouraged by American magazines’ constant rejection of his work, he took his family to England, where he found more professional success. Continuing to write about New England, he had two books published, A Boy’s Will (1913) and North of Boston (1914), which established his reputation so that his return to the United States in 1915 was as a celebrated literary figure. Holt put out an American edition of North of Boston in 1915, and periodicals that had once scorned his work now sought it. """
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