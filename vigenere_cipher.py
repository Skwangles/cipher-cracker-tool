from utils import *
import string

#
# Split the characters into columns based on key period
#
def split_text_into_columns(cipher_text: str, period: int):
    chars = 0
    columns = [''] * period

    y = range(len(cipher_text))
    for j in y:
        if (cipher_text[j].isalpha()):
            columns[chars % period] += cipher_text[chars]
            chars += 1
    return columns

#
# Get the likely key period based on index of coincidence averages.
#
def find_key_period(cipher_text: str, max_period: int):
    # Remove punctuation and spaces
    cipher_text = cipher_text.translate(str.maketrans("", "", string.punctuation)).replace(" ", "")
    # Intialise variables
    ioc_highest = 0
    period = 0

    # Compute index of coincidence on a range of key periods
    x = range(2, max_period + 1)
    for i in x:
        ioc_sum = 0
        columns = split_text_into_columns(cipher_text, i)
        
        # Computing average index of coincidence
        z = range(i)
        for k in z:
            ioc_sum += index_of_coincidence(columns[k])
        ioc_avg = ioc_sum / i

        # Find the higher than expected index of coincidence
        if (ioc_avg >= ioc_highest):
            ioc_highest = ioc_avg
            period = i
    return period

#
# Encrypts the text using key.
#
def encrypt(text: str, key: str):
    cipher_text = ""

    x = range(len(text))
    for i in x:
        char = ""
        # Encrypt a letter character
        if text[i].isalpha():
            m = ord(text[i].upper())
            k = ord(key[i].upper())
            char = chr(((m + k) % 26) + ord('A'))
        else:
            char = text[i]
        # Append character
        cipher_text += char
    print("Using key sequence '" + key + "'\n" +
          "Cipher text: " + cipher_text + "\n")
    return cipher_text

#
# Decrypts the cypher text using key.
#
def decrypt(cipher_text: str, key: str):
    original_text = ""

    x = range(len(cipher_text))
    for i in x:
        m = ""
        # Decrypt a letter character
        if text[i].isalpha():
            char = ord(cipher_text[i].upper())
            k = ord(key[i].upper())
            m = chr(((char - k) % 26) + ord('A'))
        else:
            m = text[i]
        # Append character
        original_text += m
    print("Using key sequence '" + key + "'\n" +
          "Original text: " + original_text + "\n")
    return original_text

#
# Cracks the cypher text, returning the key.
#
def crack(cipher_text):
    if not cipher_text:
        return "No cipher text"
    print("Possible key period: " + str(find_key_period(cipher_text, 10)))
    return "No key found yet"

#
# Generate the key sequence in a cyclic manner from key.
#
def generate_key_sequence(text: str, key: str):
    seq = ""
    chars = 0

    if (len(key) == len(text)):
        print("Key Sequence: " + key + "\n")
        return key
    
    x = range(len(text))
    for i in x:
        letter = " "
        # Ignore space characters
        if text[i].isalpha():
            letter = key[chars % len(key)]
            chars += 1
        seq += letter
    print("Key Sequence: '" + seq + "'\n")
    return seq

if __name__ == "__main__":
    # text = "hi. and welcome to my cypher $123"
    text = "A space explorer is unexpectedly dragged into a conflict between two factions: Kodia Accord and Nexia Syndicate. He is pressured as he has to decide who he sides with and ultimately questions the relationship with his fellow crew members."
    # text = "hello there this is cool"
    key = "crypto"
    print("Input text: " + text + "\n" +
          "Key '" + key + "'\n")
    key_seq = generate_key_sequence(text, key)
    cipher_text = encrypt(text, key_seq)
    original_text = decrypt(cipher_text, key_seq)
    print(crack(cipher_text))