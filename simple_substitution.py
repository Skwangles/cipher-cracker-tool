import random
import string

def get_english_frequencies():
    # Approximate frequency of letters in the English language.
    # You can adjust these values based on more detailed studies.
    return {
        'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,
        'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153,
        'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,
        'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
        'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974, 'z': 0.00074
    }


def generate_key():
    """Generates a random substitution key."""
    characters = list(string.ascii_lowercase)
    shuffled = random.sample(characters, len(characters))
    return ''.join(shuffled)


def encrypt(text, key):
    # Checks if user has provided key
    if not key:
        key = generate_key()
    
    # 
    characters = string.ascii_lowercase
    table = str.maketrans(characters, key)
    return text.translate(table)


def decrypt(cypher_text, key):
    """Decrypts the cypher text using the key."""
    characters = string.ascii_lowercase
    table = str.maketrans(key, characters)
    return cypher_text.translate(table)


def crack(cypher_text):
    """Cracks the cypher text using letter frequency analysis."""
    frequencies = get_english_frequencies()
    cipher_frequencies = {char: cypher_text.count(char) / len(cypher_text) for char in string.ascii_lowercase}
    
    # Sort letters in the English language by frequency
    sorted_english = sorted(frequencies.keys(), key=lambda x: frequencies[x], reverse=True)
    
    # Sort letters in the cipher by frequency
    sorted_cipher = sorted(cipher_frequencies.keys(), key=lambda x: cipher_frequencies[x], reverse=True)
    
    # Create a mapping between the cipher letter and the estimated English letter
    translation = {cipher_letter: english_letter for cipher_letter, english_letter in zip(sorted_cipher, sorted_english)}
    
    # Generate a key for decryption
    key = ''.join([translation[char] for char in string.ascii_lowercase])
    return key


key = generate_key()
plaintext = "this is a basic approach and may not work perfectly for all texts the more text that you have the more likely it will be that the text can be cracked using frequency analysis"
cyphertext = encrypt(plaintext, key)
print(f"Key: {key}")
print(f"Plaintext: {plaintext}")
print(f"Cyphertext: {cyphertext}")
print(f"Decrypted: {decrypt(cyphertext, key)}")

print(crack(cyphertext))