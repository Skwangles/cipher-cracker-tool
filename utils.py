import random, nltk
from nltk.corpus import words 

def index_of_coincidence(input):
    """Calculates the IoC"""

    if not input.isalpha():
        print("Called IoC on non-alpha string")
        return None

    # Sum occurances of letters
    letters = {}
    for i in input:
        if i in letters:
            letters[i] += 1
        else:
            letters[i] = 1

    # Calculate using algorithm from class
    sigma_f = 0
    for f in letters.items():
        sigma_f += f*(f - 1)
    big_n = len(input)
    return sigma_f/(big_n * (big_n - 1))


def xor_string_and_key(string, key):
    """XORs a string with a key - assumes both are binary strings"""
    output = ""
    for i in range(len(string)):
        if string[i] == key[i % len(key)]:
            output += '0'
        else:
            output += '1'
    return output

def string_to_binary(string):
    """Converts a string to a binary equivalent of the ascii char values"""
    # Adapted from https://www.geeksforgeeks.org/python-convert-string-to-binary/
    # get int value of ascii char, then convert to binary with 'format' and left pad to 8 bits
    return "".join(str(format(ord(i), "b").zfill(8)) for i in string)

def binary_to_string(binary):
    """Converts a binary string to a string of characters"""
    # Adapted from https://www.geeksforgeeks.org/convert-binary-to-string-using-python/
    # Split the string into 8 bit chunks, use int(<num>, 2) to get base 10 version of binary, then convert to ascii value    
    return "".join(chr(int(binary[i:i+8],2)) for i in range(0, len(binary), 8))

def random_key(length=3):
    """Generates a random key of the given length"""
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(alphabet.ascii_lowercase) for i in range(length))


#store the set of words globally so we dont have to spend ages getting them each time
english_words = None 

def get_english_percent(input):
    """Calculates the percentage of english words in a text"""

    if not input:
        print("Missing input text to calculate english word %")
        return None

    #if our global set of english words isnt available yet, go get them
    global english_words
    if not english_words:
        try:
            nltk.data.find('corpora/words.zip')
        except LookupError:
            nltk.download('words')

        english_words = set(words.words())
    

    input_words = input.split()    
        
    #search our text for english words
    english_word_count = sum(1 for word in input.split() if word.lower() in english_words)
    return round((english_word_count / len(input_words)) * 100, 2)
