import random, nltk
from nltk.corpus import words 
import sympy 


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
    try:
        return pow(A, -1, M)
    except ValueError:
        raise ValueError("No modular inverse for {} and {}".format(A, M))

def calc_e_d(p, q, e=11):
    
    fi_n = (p-1)*(q-1)
    
    if e > fi_n:
        print("fi_n is too small for default e, generating a new e")
        e = sympy.randprime(2, fi_n)
        
    d = modInverse(e, fi_n)
    return [e, d]


def get_primes(min, max, is_weak=False):
    p = sympy.randprime(min, max)
    q = 0
    if is_weak:
        q = sympy.nextprime(sympy.nextprime(p))
    else:
        q = sympy.randprime(min, max)
        while p == q:
            q = sympy.randprime(min, max)
    return [p, q]