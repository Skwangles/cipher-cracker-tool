import re

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
    hex = is_hex(hex)
    if not hex:
        raise Exception("Hex string is not a valid hex string")
    hex = str(hex)
        
    return "".join(str(format(int(hex[i],16), 'b').zfill(4)) for i in range(0, len(hex), 1))

def hex_to_string(hex):
    """Converts a hex string to a string of characters"""
    # Adapted from https://www.geeksforgeeks.org/convert-hexadecimal-value-string-ascii-value-string/
    # Iterated forward 2 at a time, use int(<num>, 16) to get base 10 version of hex, then convert to ascii value with chr
    
    hex = is_hex(hex)
    if not hex:
        raise Exception("Hex string is not a valid hex string")
    hex = str(hex)
    
    output = ""
    for i in range(0, len(hex), 2):
        output += chr(int(hex[i:i+2],16))
    return output 

def is_hex(hex):
    """Checks if a string is a valid hex string"""
    hex = str(hex).replace(" ", "")
    if re.match("[^a-fA-F0-9]+", hex):
        return False
    
    # Check if validly converts to ascii's length
    if len(hex) % 2 != 0:
        print("Called hex_to_string on non-even hex string")
        return False
    
    return hex

def string_to_hex(string):
    """Converts a string to a hex equivalent of the ascii char values"""
    # Adapted from https://www.geeksforgeeks.org/convert-a-string-to-hexadecimal-ascii-values/
    # get int value of ascii char, then convert to hex with 'format'
    output = ""
    for i in string:
        if ord(i) > 255:
            print("Called string_to_hex on non-ascii string")
            return None
        
        hexval = str(format(ord(i), "x"))
        if len(hexval) == 1:
            hexval = "0" + hexval
            
        output += hexval
    return output