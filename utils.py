def index_of_coincidence(input):
    """Calculates the IoC"""

    if not input.isalpha():
        print("Called IoC on non-alpha string")
        return None

    # Sum occurances of letters
    letters = {}
    for i in input:
        if i in letters:
            letters[i] += 1
        else:
            letters[i] = 1

    # Calculate using algorithm from class
    sigma_f = 0
    for f in letters.items():
        sigma_f += f*(f - 1)
    big_n = len(input)
    return sigma_f/(big_n * (big_n - 1))


def xor_string_and_key(string, key):
    """XORs a string with a key"""
    if len(string) != len(key):
        key = match_key_to_text_length(key, len(string))
    
    string_bin = get_binary_string(string)
    key_bin = get_binary_string(key)

    # XOR both strings
    xor_string = ""
    for i in range(len(string_bin)):
        xor_string += str(int(string_bin[i]) ^ int(key_bin[i]))

    # Convert back to string
    xor_ascii_string = ""
    for i in range(0, len(xor_string), 8):
        xor_ascii_string += chr(int(xor_string[i:i+8], 2))

    return xor_ascii_string


def pad_string_to_multiple_of(text, multiple=2):
    """Pads the string to a multiple of, default 2 - used for Feistal cipher"""
    remainder = len(text) % multiple
    if remainder == 0:
        return text
    else:
        return text + "#"*remainder


def match_key_to_text_length(key, length):
    """Repeats the key to the length specified, or trims it if too long"""
    if length< len(key):
        print("Warning: key longer than text, trimming key")
        key = key[: length]
    elif length > len(key):
        print("Warning: key shorter than text, repeating key")
        # Repeat the key to match the length of the text
        key = key * (length // len(key))
        # Trim off the excess
        key += key[:len(key)-length] # Won't add anything if same length
    return key


def get_binary_string(string):
    """Converts a string to a binary equivalent of the ascii char values"""
    string_bin = ""
    for i in string:
        string_bin += bin(ord(i))[2:] #[2:] removes the '0b' part from bin
    return string_bin


def split_string_to_list_of_even_parts(string, string_length):
    """Splits a string into a list of even parts - i.e. turning a key string into a keyspace"""
    return [string[i:i+string_length] for i in range(0, len(string), string_length)]