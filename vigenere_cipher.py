#
# Encrypts the text using key.
#
def encrypt(text: str, key: str):
    cipher_text = ""

    x = range(len(text))
    for i in x:
        char = " "
        # Encrypt a non space character
        if text[i] != " ":
            m = ord(text[i].upper())
            k = ord(key[i].upper())
            char = chr(((m + k) % 26) + ord('A'))
        # Append character
        cipher_text = cipher_text + char
    print("Using key '" + key + "'\n" +
          "Cipher text: " + cipher_text + "\n")
    return cipher_text

#
# Decrypts the cypher text using key.
#
def decrypt(cipher_text: str, key: str):
    original_text = ""

    x = range(len(cipher_text))
    for i in x:
        m = " "
        # Decrypt a non space character
        if text[i] != " ":
            char = ord(cipher_text[i].upper())
            k = ord(key[i].upper())
            m = chr(((char - k) % 26) + ord('A'))
        # Append character
        original_text = original_text + m
    print("Using key '" + key + "'\n" +
          "Original text: " + original_text + "\n")
    return original_text

#
# Cracks the cypher text, returning the key.
#
def crack(cipher_text):
    """Cracks the cypher text, returning the key"""
    return "Not implemented"

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
        if text[i] != " ":
            letter = key[chars % len(key)]
            chars = chars + 1
        seq = seq + letter
    print("Key Sequence: " + seq + "\n")
    return seq

if __name__ == "__main__":
    text = "hi and welcome to my cypher"
    key = "crypto"
    print("Input text: " + text + "\n" +
          "Key '" + key + "'\n")
    key_seq = generate_key_sequence(text, key)
    cipher_text = encrypt(text, key_seq)
    original_text = decrypt(cipher_text, key_seq)