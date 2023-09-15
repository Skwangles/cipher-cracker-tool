import sys
import argparse


# Cipher modules
import caesar_cipher
import rsa
import simple_substitution
import feistel_cipher

### --- Cipher calls

            
def call_caesar(args):
    cipher = caesar_cipher
    match args.action.lower():
        case "crack":
            print(cipher.crack(args.text))
        case "decrypt":
            print(cipher.decrypt(args.text, args.shift))
        case "encrypt":
            print(cipher.encrypt(args.text, args.shift))
        case _:
            print("Unsupported operation:", args.action)
    
def call_rsa(args):
    cipher = rsa
    match args.action.lower():
        case "crack":
            print(cipher.crack(args.text))
        case "decrypt":
            print(cipher.decrypt(args.text, args.private))
        case "encrypt":
            print(cipher.encrypt(args.text, args.public))
        case _:
            print("Unsupported operation:", args.action)

def call_simple_substitution(args):
    cipher = simple_substitution
    match args.action.lower():
        case "crack":
            print(cipher.crack(args.text))
        case "decrypt":
            print(cipher.decrypt(args.text, args.key))
        case "encrypt":
            print(cipher.encrypt(args.text, args.key))
        case _:
            print("Unsupported operation:", args.action)
    
def call_feistel(args):
    cipher = feistel_cipher
    match args.action.lower():
        case "crack":
            print(cipher.crack(args.text))
        case "decrypt":
            print(cipher.decrypt(args.text, args.keys, args.keylength, args.rounds))
        case "encrypt":
            print(cipher.encrypt(args.text, args.keys, args.keylength, args.rounds))
        case _:
            print("Unsupported operation:", args.action)
    
    
    

### ----- Arguments handling functions -----

# define command line arguments and subparsers
parser = argparse.ArgumentParser(prog="main.py", description="Encrypt, decrypt or crack a cipher text.")

# required cipher type first
individual_cipher_arg_parsers = parser.add_subparsers(title="cipher", dest="cipher", required=True, help="Cipher types - rsa, caesar, simple, feistel")

# give selection of actions - encrypt, decrypt, crack
action_group = parser.add_argument_group("action", argument_default="encrypt")
action_group.add_argument("--encrypt", "-e", action="store_const", const="encrypt", dest="action", default="encrypt", help="Encrypt the plain text")
action_group.add_argument("--decrypt", "-d", action="store_const", const="decrypt", dest="action", help="Decrypt the cipher text")
action_group.add_argument("--crack", "-c", action="store_const", const="crack", dest="action", help="Crack the cipher text")

# caesar - shift based key 0-26
caesar_parser = individual_cipher_arg_parsers.add_parser("caesar", help="Caesar Cipher")
caesar_parser.add_argument("-t","--text", required=True, help="*Text to encrypt/decrypt/crack")
caesar_parser.add_argument("-s", "--shift", default=0, type=int, choices=range(0, 27), help="Caesar shift (0-26)")

# rsa
rsa_parser = individual_cipher_arg_parsers.add_parser("rsa", help="RSA Cipher")
rsa_parser.add_argument("-t","--text", required=True, help="*Text to encrypt/decrypt")
rsa_parser.add_argument("-k", "--private", help="Private key")
rsa_parser.add_argument("-p", "--public", help="Public key")

# simple sub - text based key
simple_parser = individual_cipher_arg_parsers.add_parser("simple", help="Simple Substitution Cipher")
simple_parser.add_argument("-t","--text", required=True, help="*Text to encrypt/decrypt")
simple_parser.add_argument("-k", "--key", default="abcdefghijklmnopqrstuvwxyz", help="Substitution key - default: 'abcdefghijklmnopqrstuvwxyz'")

# feistel - text based key, rounds integer, and keylength integer
feistel_parser = individual_cipher_arg_parsers.add_parser("feistel", help="Feistel Cipher")
feistel_parser.add_argument("-t","-b","--text", "--binary", required=True, dest="text", help="Plaintext to encrypt/Binary to decrypt")
feistel_parser.add_argument("-k", "--keys", default="abc123hij", help="Key string - default: 'abc123hij' (w/ keylength 3) ")
feistel_parser.add_argument("-l", "--keylength", default=3, help="# chars in individual round keys - the key string's length must be a multiple of this number - default: 3", type=int)
feistel_parser.add_argument("-r", "--rounds", default=16, help="# of rounds to run the feistel cipher for - default: 16", type=int)

def main():
    prog_args = parser.parse_args()

    cipher_type = None
    match prog_args.cipher.lower():
        case "rsa":
            call_rsa(prog_args)
        case "caesar":
            call_caesar(prog_args)
        case "simple":
            call_simple_substitution(prog_args)
        case "feistel":
            call_feistel(prog_args)
        case _:
            print("Unsupported cipher type:", prog_args.cipher)
            sys.exit(1)
                

if __name__ == "__main__":
    main()
