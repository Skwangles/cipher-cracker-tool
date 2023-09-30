def string_to_binary(string):
    """Converts a string to a binary equivalent of the ascii char values"""
    # Adapted from https://www.geeksforgeeks.org/python-convert-string-to-binary/
    # get int value of ascii char, then convert to binary with 'format' and left pad to 8 bits
    return "".join(str(format(ord(i), "b").zfill(8)) for i in string)

def binary_to_string(binary):
    """Converts a binary string to a string of characters"""
    # Adapted from https://www.geeksforgeeks.org/convert-binary-to-string-using-python/
    # Split the string into 8 bit chunks, use int(<num>, 2) to get base 10 version of binary, then convert to ascii value    
    return "".join(chr(int(binary[i:i+8],2)) for i in range(0, len(binary), 8))

def binary_to_hex(binary):
    """Converts a binary string to a hex string"""
    # Split the string into 4 bit chunks, use int(<num>, 2) to get base 10 version of binary, then convert to hex value
    return "".join(hex(int(binary[i:i+4],2))[2:] for i in range(0, len(binary), 4))

def hex_to_binary(hex):
    """Converts a hex string to a binary string"""
    # Split the string into 1 hex chunks, use format(<num>, 'b') to get binary version of hex, then left pad to 4 bits
    return "".join(str(format(int(hex[i],16), 'b').zfill(4)) for i in range(0, len(hex), 1))