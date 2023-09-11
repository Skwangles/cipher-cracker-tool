def encrypt(text, key):
    keySequence = generateKeySequence(key, text)
    # print(keySequence)
    """Encrypts the text using the key"""
    return "Not implemented"

def decrypt(cypher_text, key):
    """Decrypts the cypher text using the key"""
    return "Not implemented"

def crack(cypher_text):
    """Cracks the cypher text, returning the key"""
    return "Not implemented"

def generateKeySequence(key, text):
    seq = list(key)
    if (len(seq) == len(text)):
        return key
    
    x = range(len(text) - len(seq))
    for i in x:
        letter = seq[i % len(text)]
        seq.append(letter)
    return "" . join(seq)

# if __name__ == "__main__":
#     encrypt("hellothere", "apps")