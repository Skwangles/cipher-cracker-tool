def encrypt(text, key):
    """Encrypts the text using the key"""
    
    encrypted = ""
    for char in text:

        if char.isalnum():
            # lowercase by default but handle uppercase and digits
            baseChar = 'a'
            setLength = 26

            if char.isupper():
                baseChar = 'A'

            elif char.isdigit():
                baseChar = '0'
                setLength = 10
        
            offset = (ord(char) - ord(baseChar) + int(key)) % setLength
            encrypted += chr(offset + ord(baseChar))
        
        #leave non-alphanumeric characters unchanged
        else: encrypted += char
            
    return encrypted


def decrypt(cipher_text, key):
    """Decrypts the cypher text using the key"""
    #encrypting with the negative key is the same as decrypting
    return encrypt(cipher_text, -int(key)) 


def crack(cypher_text):
    """Cracks the cypher text, returning the key"""
    return "Not implemented"
