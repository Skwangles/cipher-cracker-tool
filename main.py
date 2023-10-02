import sys
import argparse


# Cipher modules
import caesar_cipher
import rsa
import simple_substitution
import feistel_cipher
import elgamal

### --- Cipher calls

            
def call_caesar(args):
    cipher = caesar_cipher
    match args.action.lower():
        case "crack":
            print(cipher.crack(args.text, args.digits))
        case "decrypt":
            print(cipher.decrypt(args.text, args.shift, args.digits))
        case "encrypt":
            print(cipher.encrypt(args.text, args.shift, args.digits))
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
            print(cipher.decrypt(args.text, args.key, args.rounds))
        case "encrypt":
            print(cipher.encrypt(args.text, args.key, args.rounds))
        case _:
            print("Unsupported operation:", args.action)

def call_elgamal(args):
    cipher = elgamal
    match args.action.lower():
        case "crack":
            print(cipher.crack(args.text, args.text2, args.receiver, args.root, args.modulus))
        case "decrypt":
            print(cipher.decrypt(args.text, args.text2, args.private, args.root, args.modulus))
        case "encrypt":
            print(args)
            print(cipher.encrypt(args.text, args.receiver, args.root, args.modulus, args.little_k if args.little_k else -1 ))
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
caesar_parser.add_argument("-s", "--shift", default=0, type=int, choices=range(-26, 27), help="Caesar shift ±(0-26)")
caesar_parser.add_argument("-d", "--digits", action="store_true", help="Shift the digits in addition to characters")

# rsa
rsa_parser = individual_cipher_arg_parsers.add_parser("rsa", help="RSA Cipher")
rsa_parser.add_argument("-t","--text", required=True, help="*Text to encrypt/decrypt")
rsa_parser.add_argument("-k", "--private", help="Private key")
rsa_parser.add_argument("-p", "--public", help="Public key")

# elgamal
elgamal_parser = individual_cipher_arg_parsers.add_parser("elgamal", help="RSA Cipher")
elgamal_parser.add_argument("-t", "-t1","--text", "--text1", required=True, help="Text to encrypt")
elgamal_parser.add_argument("-t2","--text2", help="Text Km to decrypt (Decrypt/Crack)")
elgamal_parser.add_argument("-k", "--little-k", help="Little k/random number (Encrypt optional)")
elgamal_parser.add_argument("-y", "--receiver", help="Receiver's y value (Encrypt/Crack)")
elgamal_parser.add_argument("-b", "-x", "--private", help="Receiver's private key (Decrypt)")
elgamal_parser.add_argument("-a", "-r", "--root", required=True, help="Root value")
elgamal_parser.add_argument("-p", "--modulus", required=True, help="Modulus value")


# simple sub - text based key
simple_parser = individual_cipher_arg_parsers.add_parser("simple", help="Simple Substitution Cipher")
simple_parser.add_argument("-t","--text", required=True, help="*Text to encrypt/decrypt")
simple_parser.add_argument("-k", "--key", default="abcdefghijklmnopqrstuvwxyz", help="Substitution key - default: 'abcdefghijklmnopqrstuvwxyz'")

# feistel - text based key, rounds integer, and keylength integer
feistel_parser = individual_cipher_arg_parsers.add_parser("feistel", help="Feistel Cipher")
feistel_parser.add_argument("-t","-b","--text", "--binary", required=True, dest="text", help="Plaintext to encrypt/Binary to decrypt")
feistel_parser.add_argument("-k", "--key", default="abc123", help="Key - default: 'abc123' ")
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
        case "elgamal":
            call_elgamal(prog_args)
        case _:
            print("Unsupported cipher type:", prog_args.cipher)
            sys.exit(1)
                

if __name__ == "__main__":
    main()
