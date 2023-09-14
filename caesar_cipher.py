def encrypt(text, key):
    """Encrypts the text using the key"""
    
    encrypted = ""
    for char in text:

        if char.isalnum():
            # lowercase by default. also handle uppercase and digits 0-9
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
    """Decrypts the cipher text using the key"""

    #encrypting with the negative key is the same as decrypting
    return encrypt(cipher_text, -int(key)) 


#uses brute force, but a TODO could be to also use letter frequency analysis on these to select the most probable text/key
def crack(cipher_text):
    """Cracks the cipher text using brute force, returning all the possible texts and keys. The user must identify the correct one."""
    
    shifts = ""

    #optimisation: if theres no alpha character, only need to test for digits
    if any(char.isalpha() for char in cipher_text): setLength = 26
    else: setLength = 10

    #try all possible shifts (1 to 25)
    for key in range(1,setLength):  
            decrypted_text = decrypt(cipher_text, key)
            shifts += (f"key {key}: '{decrypted_text.encode('utf-8').decode('utf-8', 'ignore')}'") + "\n"

    return shifts[:-1] #take away last newline