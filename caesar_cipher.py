import nltk
from nltk.corpus import words 


def encrypt(text, key):
    """Encrypts the text using the key"""
    
    encrypted = ""
    for char in text:

        if char.isalnum():
            #lowercase by default. also handle uppercase and digits 0-9
            base_char = 'a'
            set_length = 26

            if char.isupper():
                base_char = 'A'

            elif char.isdigit():
                base_char = '0'
                set_length = 10
        
            offset = (ord(char) - ord(base_char) + int(key)) % set_length
            encrypted += chr(offset + ord(base_char))
        
        #leave non-alphanumeric characters unchanged
        else: encrypted += char
            
    return "'" + encrypted + "'" #surround in single quotes to show any whitespace at the end or start


def decrypt(cipher_text, key):
    """Decrypts the cipher text using the key"""

    #encrypting with the negative key is the same as decrypting
    return encrypt(cipher_text, -int(key)) 


#uses brute force and english word counting to sort the output by most probable to least probable decrypt key
def crack(cipher_text):
    """Cracks the cipher text using brute force, returning all the possible texts and keys, sorted by number of matching english words"""
    
    #get english words if not already downloaded
    try:
        nltk.data.find('corpora/words.zip')
    except LookupError:
        nltk.download('words')
        
    english_words = set(words.words())

    #optimisation: if theres no alpha characters, only need to crack for digits
    if any(char.isalpha() for char in cipher_text): set_length = 26
    else: set_length = 10

    #try all possible shifts
    results = []
    for key in range(1,set_length):  
        decrypted_text = decrypt(cipher_text[1:-1], key)[1:-1] #test decrypt with that key. remove first and last apostrophes
        decrypted_words = decrypted_text.split()

        #count number of matching english words
        english_word_count = sum(1 for word in decrypted_words if word.lower() in english_words)
        results.append((key, decrypted_text, english_word_count))

    #sort by english word count descending
    results.sort(key=lambda result: result[2], reverse=True) 

    #make the results more readable for console output
    readable_results = '\n'.join(f"key: {key}\t\ttext: '{text}'\t\tenglish words: {word_count}" for key, text, word_count in results)
    return readable_results

if __name__ == "__main__":
    print("Test encrypt")
    print(encrypt("abc", 1))
    print(encrypt("abc", 2))        

    print("Test decrypt")
    print(decrypt("bcd", 1))
    print(decrypt("cde", 2))
    
    print("Test crack")
    print("Simple crack")
    print(crack(encrypt("the best part of life is the way it ends even when cheese is full of hate", 5)))
    print(crack(encrypt("""Those hours that with gentle work did frame
  The lovely gaze where every eye doth dwell
  Will play the tyrants to the very same,
  And that unfair which fairly doth excel:
  For never-resting time leads summer on
  To hideous winter and confounds him there,
  Sap checked with frost and lusty leaves quite gone,
  Beauty o'er-snowed and bareness every where:
  Then were not summer's distillation left
  A liquid prisoner pent in walls of glass,
  Beauty's effect with beauty were bereft,
  Nor it nor no remembrance what it was.
    But flowers distilled though they with winter meet,
    Leese but their show, their substance still lives sweet.""", 5)))
    