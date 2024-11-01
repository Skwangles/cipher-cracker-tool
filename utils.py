import random, nltk
from nltk.corpus import words 
import sympy 
from math import log10
import re

# Quadgram scoring function
# Adapted from http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/
quadgrams = {}
total_nums = 0
for line in open('english_quadgrams.txt'):
    key,count = line.split(' ') 
    total_nums += int(count)
    quadgrams[key.upper()] = int(count)
    
# convert count to log probabilities
for key in quadgrams.keys():
    quadgrams[key] = log10(float(quadgrams[key])/total_nums)

#what log probability to give a new quadgram
floor = log10(0.01/total_nums) 

def get_english_score(text):
    score = 0
    text = re.sub("[^A-Za-z]", "", text).upper()
    for i in range(len(text)-4+1):
        if text[i:i+4] in quadgrams: 
            score += quadgrams[text[i:i+4]]
        else: 
            score += floor
    return score


def index_of_coincidence(input):
    """Calculates the IoC"""

    # Sum occurances of letters
    letters = {}
    len_alpha_input = 0
    for i in input:
        if str(i).isalpha():
            i = str(i).upper()
            len_alpha_input += 1
            if i in letters:
                letters[i] += 1
            else:
                letters[i] = 1

    if len_alpha_input == 0:
        # No alpha chars to count
        return 0

    # Calculate using algorithm from class
    sigma_f = 0
    for f in letters.items():
        sigma_f += f[1] * (f[1] - 1)
    big_n = len_alpha_input
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


#store the set of words globally so we dont have to spend ages getting them each time
english_words = None 

def get_english_percent(input):
    """Calculates the percentage of english words in a text"""

    if not input:
        print("Missing input text to calculate english word %")
        return None
    
    #punctionation and numbers arent part of english words, so remove them
    input = re.sub("[^A-Za-z\\s]", "", input).lower()

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


# just count number of possible words in the text. overlap with other words not checked if no spaces
def get_english_word_count(input):
    """Counts the number of english words in a piece of text"""

    if not input:
        print("Missing input text to calculate english word count")
        return None
    
    #punctionation and numbers arent part of english words, so remove them
    input = re.sub("[^A-Za-z\\s]", "", input).lower()

    #if our global set of english words isnt available yet, go get them
    global english_words
    if not english_words:
        try:
            nltk.data.find('corpora/words.zip')
        except LookupError:
            nltk.download('words')

        english_words = set(words.words())
    
    
    #normal case. spaced-words
    if ' ' in input:  
        #search our text for english words
        return sum(1 for word in input.split() if word in english_words)
    
    #no spaces: count dictionary words
    else:
        english_word_count = 0
        sum_word_lengths = 0 #dont need to store individual words
        
        for word in english_words:
            if word.lower() in input:
                english_word_count += 1
                sum_word_lengths += len(word)

        return english_word_count

def get_alphabet():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return alphabet


def get_random_number(min=0, max=100):
    """Returns a random number between min and max"""
    return random.randint(min, max)


def frequency_analysis(cipher_text):
    """Returns frequencies of each letter in a string"""   
    # Count each letter's frequency in the ciphertext
    letter_freq = {}
    for letter in cipher_text:
        if letter.isalpha():
            letter = letter.upper()
            if letter not in letter_freq:
                letter_freq[letter] = 1
            else:
                letter_freq[letter] += 1

    # Sort letters by frequency
    sorted_freq = sorted(letter_freq, key=letter_freq.get, reverse=True)
    sorted_freq = ''.join(sorted_freq)

    return sorted_freq


def modInverse(A, M):
    """Utilise built in pow function to calculate modular inverse - notify user if no inverse exists"""
    try:
        return pow(A, -1, M)
    except ValueError:
        # Raise a more helpful error message - which includes the numbers that were used
        raise ValueError("No modular inverse for {} and {}".format(A, M))
