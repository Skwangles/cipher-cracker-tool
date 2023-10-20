from utils import get_english_word_count

def encrypt(text, key, shift_digits=False):
    """Encrypts the text using the key. Optionally shift digits as well as letters"""
    
    encrypted = ""
    for char in text:

        if char.isalpha():
            base_char = 'a' if char.islower() else 'A'
            set_length = 26
        
        elif char.isdigit() and shift_digits:
            base_char = '0'
            set_length = 10
        
        if char.isalpha() or (char.isdigit() and shift_digits):
            offset = (ord(char) - ord(base_char) + int(key)) % set_length
            encrypted += chr(offset + ord(base_char))

        #leave non-alphanumeric characters unchanged
        else: encrypted += char

    return "'" + encrypted + "'" #surround in single quotes to show any whitespace at the end or start


def decrypt(cipher_text, key, shift_digits=False):
    """Decrypts the cipher text using the key"""

    #encrypting with the negative key is the same as decrypting
    return encrypt(cipher_text, -int(key), shift_digits) 


#uses brute force and english word counting to sort the output by most probable to least probable decrypt key
def crack(cipher_text, shift_digits=False):
    """Cracks the cipher text using brute force, returning all the possible texts and keys, sorted by number of matching possible english words"""
    
    #check for empty inputs
    if not cipher_text or len(cipher_text) == 2 and cipher_text[0] == cipher_text[1] == "'": return "Empty cipher text. Nothing to crack"
        
    #optimisation: if theres no alpha characters, only need to crack for digits
    if any(char.isalpha() for char in cipher_text): set_length = 26
    else: set_length = 10

    #try all possible shifts
    results = []
    for key in range(1,set_length):
        #test decrypt with that key. clean up apostrophes in input if applicable
        if len(cipher_text) > 0 and cipher_text[0] == cipher_text[len(cipher_text)-1] == "'":
            decrypted_text = decrypt(cipher_text[1:-1], key, shift_digits)[1:-1]
        else: 
            decrypted_text = decrypt(cipher_text, key, shift_digits)[1:-1]

        #count eng words for readability check
        eng_word_count = get_english_word_count(decrypted_text)
        results.append((key, decrypted_text, eng_word_count))

    results.sort(key=lambda result: result[2], reverse=True)

    #if one result is more english than the rest, only show that result
    if results[0][2] > results[1][2]:
        key, text, english_count = results[0]
        return f"key: {key}\t\ttext: '{text}'\t\tenglish words: {english_count}"
    
    #show all results with some english if none is the best
    elif results[0][2] == results[1][2] and results[0][2] > 0:
        non_zero_results = [(key, text, english_count) for key, text, english_count in results if english_count > 0]
        if non_zero_results:
            return '\n'.join(f"key: {key}\t\ttext: '{text}'\t\tenglish words: {english_count}" for key, text, english_count in non_zero_results)

    #case: no english. show all results
    else:
        return '\n'.join(f"key: {key}\t\ttext: '{text}'\t\tenglish words: {english_count}" for key, text, english_count in results)
     

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

    print("Test crack: no best result")
    print(crack(encrypt("egg 1", 13)))

    print("Test crack: no english words")
    print(crack(encrypt("arst", -1)))

    print("Test crack: empty input")
    print(crack(encrypt("", 1)))

    print("Test encrypt/decrypt: include digits")
    print(encrypt("the fat cat sat on the mat 12345", 2, True))
    print(decrypt("vjg hcv ecv ucv qp vjg ocv 34567", 2, True))

    print("no spaces crack")
    print(crack("pohcltfzlsmmbssjvumpklujlaohapmhsskvaolpykbafpmuvaopunpzulnsljalkhukpmaolilzahyyhunltluazhylthklhzaolfhylilpunthkldlzohsswyvclvbyzlsclzvujlhnhpuhislavklmlukvbypzshukovtlavypklvbaaolzavytvmdhyhukavvbaspclaoltluhjlvmafyhuufpmuljlzzhyfmvyflhyzpmuljlzzhyfhsvulhahufyhalaohapzdohadlhylnvpunavayfavkvaohapzaolylzvsclvmopzthqlzafznvclyutlualclyfthuvmaoltaohapzaoldpssvmwhysphtluahukaoluhapvuaoliypapzoltwpylhukaolmylujoylwbispjspurlkavnlaolypuaolpyjhbzlhukpuaolpyullkdpssklmlukavaolklhaoaolpyuhapclzvpshpkpu"))