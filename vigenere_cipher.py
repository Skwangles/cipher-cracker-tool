#
# Encrypts the text using key.
#
def encrypt(text: str, key: str):
    cipher_text = ""

    x = range(len(text))
    for i in x:
        m = ord(text[i].upper())
        k = ord(key[i].upper())
        char = ((m + k) % 26) + ord('A')
        cipher_text = cipher_text + chr(char)
    print(cipher_text)
    return cipher_text

#
# Decrypts the cypher text using key.
#
def decrypt(cypher_text: str, key: str):
    original_text = ""

    x = range(len(cypher_text))
    for i in x:
        char = ord(cypher_text[i].upper())
        k = ord(key[i].upper())
        m = ((char - k) % 26) + ord('A')
        original_text = original_text + chr(m)
    print(original_text)
    return original_text

#
# Cracks the cypher text, returning the key.
#
def crack(cypher_text):
    """Cracks the cypher text, returning the key"""
    return "Not implemented"

#
# Generate the key sequence in a cyclic manner from key.
#
def generate_key_sequence(text: str, key: str):
    seq = list(key)
    if (len(seq) == len(text)):
        return key
    
    x = range(len(text) - len(seq))
    for i in x:
        letter = seq[i % len(text)]
        seq.append(letter)
    return "" . join(seq)

# if __name__ == "__main__":
#     text = "hiandwelcometomycypher"
#     key = "crypto"
#     key_seq = generate_key_sequence(text, key)
#     cypher_text = encrypt(text, key_seq)
#     original_text = decrypt(cypher_text, key_seq)