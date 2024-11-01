from utils import *
from itertools import product
import string
import re

# The alphabet in order of most common to least common.
ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
# The alphabet is regular order.
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Maximum value it checks for key period.
REASONABLE_MAX_PERIOD = 10
# Index of coincidence of English.
ENGLISH_IOC = 0.67

def split_text_into_columns(cipher_text: str, period: int):
    """Split the characters into columns based on key period."""
    # Initialise number of columns
    chars = 0
    columns = [''] * period

    # Split text into columns
    y = range(len(cipher_text))
    for j in y:
        if (cipher_text[j].isalpha()):
            columns[chars % period] += cipher_text[chars]
            chars += 1
    return columns

def remove_spaces_punctuation(cipher_text: str):
    """Return cipher text without spaces and punctuation characters."""
    return re.sub("[^a-zA-Z0-9]+", "", cipher_text)

def find_key_period(cipher_text: str, max_period: int):
    """Get the likely key period based on index of coincidence averages."""
    # Remove punctuation and spaces
    if not cipher_text.isalpha():
        cipher_text = remove_spaces_punctuation(cipher_text)
        
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

def get_english_frequency_match(text: str):
    """Get amount of frequency matches compared to the English frequency analysis."""
    # Extract the six most and least common letters in ordered English frequency analysis
    six_most_common_letters = ETAOIN[:6]
    six_least_common_letters = ETAOIN[-6:]

    # Initialise variables
    frequency_letters_ordered = ""
    frequencies = {
        'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0,
        'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0,
        'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0,
        'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0,
        'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0,
        'Z': 0
    }
    dictionary = {}
    match_count = 0
    
    # Count number of times a letter occurs in a given text
    for letter in text:
        if letter in frequencies:
            frequencies[letter] += 1

    # Map the letter to frequency number
    for letter in ALPHABET:
        if frequencies[letter] not in dictionary:
            dictionary[frequencies[letter]] = [letter]
        else:
            dictionary[frequencies[letter]].append(letter)

    # Join letters with the same frequency number
    for frequency in dictionary:
        dictionary[frequency].sort(key=ETAOIN.find, reverse=True)
        dictionary[frequency] = "".join(dictionary[frequency])
    
    # Sort the list in order of most frequent to least frequent
    frequency_pairs = list(dictionary.items())
    frequency_pairs.sort(reverse=True)

    # Convert frequency list into a string
    for frequency in frequency_pairs:
        frequency_letters_ordered += frequency[1]

    # Count number of times the six most common letters are in the six most frequent letters in a given text
    for letter in six_most_common_letters:
        if letter in frequency_letters_ordered[:6]:
            match_count += 1

    # Count number of times the six least common letters are in the six least frequent letters in a given text
    for letter in six_least_common_letters:
        if letter in frequency_letters_ordered[-6:]:
            match_count += 1
    return match_count

def encrypt(text: str, key: str):
    """Encrypts the text using key."""
    cipher_text = ""
    key = generate_key_sequence(text, key)

    # Iterate through each character in the text
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
    return cipher_text

def decrypt(cipher_text: str, key: str):
    """Decrypts the cypher text using key."""
    original_text = ""
    key = generate_key_sequence(cipher_text, key)

    # Iterate through each character in the cipher text
    x = range(len(cipher_text))
    for i in x:
        m = ""
        # Decrypt a letter character
        if cipher_text[i].isalpha():
            char = ord(cipher_text[i].upper())
            k = ord(key[i].upper())
            m = chr(((char - k) % 26) + ord('A'))
        else:
            m = cipher_text[i]
        # Append character
        original_text += m
    return original_text

def crack(cipher_text):
    """Cracks the cypher text, returning the key."""
    if not cipher_text:
        return "No cipher text"
    
    period = find_key_period(cipher_text, REASONABLE_MAX_PERIOD)
    cipher_text_modified = remove_spaces_punctuation(cipher_text)
    columns = split_text_into_columns(cipher_text_modified, period)
    possible_combinations = 1
    highest_ioc_key = { 
        "key": "",
        "text": "",
        "ioc": 0,
    }
    most_likely_subkeys = []
    keys = []

    # Get potential subkeys from every column
    for column in columns:
        highest_match_letters = []
        frequency_match = []
        highest_match_number = 0
        
        # Get the match count for every letter in the alphabet
        for i in ALPHABET:
            temp_key = generate_key_sequence(column, i)
            decrypted_column = decrypt(column, temp_key)
            match = get_english_frequency_match(decrypted_column)
            frequency_match.append(match)
        
        # Get the highest frequency match number
        for i in range(len(ALPHABET)):
            if frequency_match[i] > highest_match_number:
                highest_match_number = frequency_match[i]

        # Get all the letters with the highest frequency match number
        for i, letter in enumerate(ALPHABET):
            if frequency_match[i] == highest_match_number:
                highest_match_letters.append(letter)
        
        # Append these letters as likely subkeys
        most_likely_subkeys.append(highest_match_letters)
    
    # Count number of possible key combinations
    for subkey_column in most_likely_subkeys:
        possible_combinations *= len(subkey_column)
    
    # Brute force each key and find its index of coincidence
    for i in product(*most_likely_subkeys):
        key = "".join(i)
        key_sequence = generate_key_sequence(cipher_text, key)
        decrypted_text = decrypt(cipher_text, key_sequence)
        ioc = index_of_coincidence(remove_spaces_punctuation(decrypted_text))
        keys.append({ 
            "key": key,
            "text": decrypted_text,
            "ioc": ioc,
        })
        if ioc >= ENGLISH_IOC:
            return key

    # Key with the highest index of coincidence is the likely the correct key
    for k in keys:
        if k["ioc"] > highest_ioc_key["ioc"]:
            highest_ioc_key = k
    highest_ioc_key["period"] = period
    highest_ioc_key["combinations"] = possible_combinations
    return highest_ioc_key

def generate_key_sequence(text: str, key: str):
    """Generate the key sequence in a cyclic manner from key."""
    seq = ""
    chars = 0
    
    # Return key if length of both strings are equal
    if (len(key) == len(text)):
        return key
    
    # Cycle through the key
    x = range(len(text))
    for i in x:
        letter = " "
        # Ignore non alphabetic characters
        if text[i].isalpha():
            letter = key[chars % len(key)]
            chars += 1
        seq += letter
    return seq

if __name__ == "__main__":
    text = "Building a dream from your memory is the easiest way of losing your grasp on what's real and what is a dream."
    key = "dreams"

    print("\n--------------" + 
          "\nINITIALISATION" +
          "\n--------------\n" + 
          "\nInput text:\n" + text + "\n"
          "\nKey:\n'" + key + "'\n")

    cipher_text = encrypt(text, key)
    print("\n----------" + 
          "\nENCRYPTION" +
          "\n----------\n" +
          "\nCipher Text:\n" + cipher_text + "\n")

    original_text = decrypt(cipher_text, key)
    print("\n----------" + 
          "\nDECRYPTION" +
          "\n----------\n" +
          "\nOriginal Text:\n" + original_text + "\n")

    cracked_key = crack("L LLWS, GPYSOJ, QVZF TUBIMOFBWV ZVDX TG OFC JC WLPJF XLZM, LJ YPHBZTU LW YFUFVIHHH, LOR CW ZVH FPTH UIXOQKPNSHKY OUI XBRY, RY HKIJ BFY SKWQK XBRY, NK GKEWM DLFBS RYCTSFMKG RRNF OAROB DFWF HI UKTHRO PIL ZYZDRO ICGV, ZC UMOF COK ZVH WEPFG FL KDV, LOR NF UIWPTWS NYK AHRLDS IW ZMUEYOM, CW TSFIDTOLP LCU CPBFM, ZL BHGPTGUIE OOSYF. ON RTM UEEF, HBRZ WV ASBH QV GFH KZJBA KU HUC EP RI. KNOW MD UVY IKGRPGF CZ YOG PEIFGNP'Y URZPSBGVTH, HZPSM GRT CI XSFA. NYGH LW EIS QZRZ RJ ABFFZGAHRE BBX KNS QEEJCH. KNS EVTUWMY KASMCF OHU ZVH JCFBWY XSSYMMWW, COBNIO UCAVZVHV TO HBVOF FEFTS UEJ WQ XSFWL EKSG, ATMZ XVLSQH EP HBV JSDXS UVYZX BDXTWS MFOZ, DMOJBA VGQK SEISL COYH KZPR WFSFDHPT HI KNS XXXPGN FL HKITS GNIKBJXS. FJYE ZVRYRI ZUIMS WVLDHM FL SXVZQS UEJ ADRJ PZX RTR IEXPIM JZOWID IOPV LOOPPO CL DGM IEWM WHKU HKI RSWJ FL HKI RFGNRVC DRO BZF KNS RHTPIM RVDDVLUIM FL BDDT SIFV, CS VLLMZ HFZ TOER PF ZROZ. ZI DIOFC MC RR EP HBV KBG, AP TVUCR TLKSU WH WXOQGP, XS MYGZO JTHVN FT HKI DFOM RTR RGPBBM, NK GKEWM TCXNH ZMEI ULFCWQK NPBZZJSQGP BBX XXCZMYH GNIKBJXS JB NYK OLV, HF GBRRZ GIQFBX FAF LWWBBX, NNOWIGFF NYK QRWE NOS SK, KH WSBZF WOUKX ZO HBV HSDGSFG, QV YVDPW GWAYZ CQ XSF ZUEJWQK RSCOEJG, ZI DIOFC LWJLE JB NYK TLIWEG UEJ WQ XSF GNIKSWW, HF GBRRZ IMRIH CE ZVH LTMZM; NK GKEWM BYMKF VYCSSHUKF, DRO FJYE OT, ZLTDV C UU BRX QPF U DUAHRE CSFZKJH, XSJG CJROQH ZS O FRXUH TLSH IW OH ZICF GOSDIJEEFR UEJ GWECWWHX, ZVHR ZVF YDVWUI MFMIEJ HKI DFOM, RXAHH LOR ALGFGIO CM NYK PUMEJGB WRSHX, HPIFU IOUVJ PB NYK GWVFHUFV, ABWMW, JB AFJ'G JSZE HCDK, HKI YFK QFXZG, ATUV UCR WWW APKYI GBG QTHVN, JZSSW QPFNY ZC WLP SSMTAS DRO UVY COPHVLUWIE UT WLP PZX.")
    print("\n------------------------" +
          "\nCRACKING VIGENERE CIPHER" +
          "\n------------------------\n" +
          "\nPossible Key Period:\n" + str(cracked_key["period"]) +
          "\nPossible Key Combinations:\n" + str(cracked_key["combinations"]) + "\n" + 
          "\nKey:\n'" + cracked_key["key"] + "'\n" +
          "\nText:\n" + cracked_key["text"] + "\n")