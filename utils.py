import random

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
    # From https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/ - Daniel confirmed okay to use
    m0 = M
    y = 0
    x = 1
 
    if (M == 1):
        return 0
 
    while (A > 1):
 
        # q is quotient
        q = A // M
 
        t = M
 
        # m is remainder now, process
        # same as Euclid's algo
        M = A % M
        A = t
        t = y
 
        # Update x and y
        y = x - q * y
        x = t
 
    # Make x positive
    if (x < 0):
        x = x + m0
 
    return x
