import sys
import argparse


# Cipher modules
import caesar_cipher
import rsa
import simple_substitution
import feistel_cipher
import elgamal
import massey_omura

### --- Cipher calls

            
def call_caesar(args):
    cipher = caesar_cipher
    match args.action.lower():
        case "crack":
            print(cipher.crack(str(args.text), bool(args.digits)))
        case "decrypt":
            print(cipher.decrypt(str(args.text), int(args.shift), bool(args.digits)))
        case "encrypt":
            print(cipher.encrypt(str(args.text), int(args.shift), bool(args.digits)))
        case _:
            print("Unsupported operation:", args.action)
            
def call_rsa(args):
    cipher = rsa
    match args.action.lower():
        case "crack":
            print(cipher.crack(int(args.text), int(args.n), int(args.e)))
        case "decrypt":
            print(cipher.decrypt(int(args.text), int(args.n), int(args.d)))
        case "encrypt":
            print(cipher.encrypt(int(args.text), int(args.n), int(args.e))) #p and q are optional
        case "generate":
            print(cipher.generate_key(int(args.min), int(args.max)))
        case _:
            print("Unsupported operation:", args.action)
            
def call_massey_omura(args):
    cipher = massey_omura
    match args.action.lower():
        case "crack":
            print(cipher.crack(int(args.step1), int(args.step2), int(args.step3), int(args.prime)))
        case "decrypt":
            print(cipher.decrypt(int(args.text), int(args.receiver), int(args.prime)))
        case "encrypt":
            print(cipher.encrypt(int(args.text), int(args.sender), int(args.receiver), int(args.prime)))
        case _:
            print("Unsupported operation:", args.action)

def call_simple_substitution(args):
    cipher = simple_substitution
    match args.action.lower():
        case "crack":
            print(cipher.crack(str(args.text)))
        case "decrypt":
            print(cipher.decrypt(str(args.text), str(args.key)))
        case "encrypt":
            print(cipher.encrypt(str(args.text), str(args.key)))
        case _:
            print("Unsupported operation:", args.action)
    
def call_feistel(args):
    cipher = feistel_cipher
    match args.action.lower():
        case "crack":
            print(cipher.crack(str(args.text)))
        case "decrypt":
            print(cipher.decrypt(str(args.text), str(args.key), int(args.rounds)))
        case "encrypt":
            print(cipher.encrypt(str(args.text), str(args.key), int(args.rounds)))
        case _:
            print("Unsupported operation:", args.action)

def call_elgamal(args):
    cipher = elgamal
    match args.action.lower():
        case "crack":
            print(cipher.crack(int(args.text), int(args.text2), int(args.receiver), int(args.root), int(args.modulus)))
        case "decrypt":
            print(cipher.decrypt(int(args.text), int(args.text2), int(args.private), int(args.root), int(args.modulus)))
        case "encrypt":
            print(cipher.encrypt(int(args.text), int(args.receiver), int(args.root), int(args.modulus), int(args.little_k if args.little_k else -1) ))
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
action_group.add_argument("--generate", "-g", action="store_const", const="generate", dest="action", help="Generate a key")

# caesar - shift based key 0-26
caesar_parser = individual_cipher_arg_parsers.add_parser("caesar", help="Caesar Cipher")
caesar_parser.add_argument("-t","--text", required=True, help="*Text to encrypt/decrypt/crack")
caesar_parser.add_argument("-s", "--shift", default=0, type=int, choices=range(-26, 27), help="Caesar shift ±(0-26)")
caesar_parser.add_argument("-d", "--digits", action="store_true", help="Shift the digits in addition to characters")

# rsa
rsa_parser = individual_cipher_arg_parsers.add_parser("rsa", help="RSA Cipher")
rsa_parser.add_argument("-t","--text", help="Text to encrypt/decrypt", type=int)
rsa_parser.add_argument("-n", "--n", help="N value from p*q (Encrypt/Decrypt/Crack)", type=int)
rsa_parser.add_argument("-e", "--e", help="E value (inverse of d) (Encrypt/Crack)", type=int)
rsa_parser.add_argument("-d", "--d", help="D value (Private) (Decrypt)", type=int)
rsa_parser.add_argument("-p", "--p", help="P value (Encrypt - not required if N provided)", type=int)
rsa_parser.add_argument("-q", "--q", help="Q value (Encrypt - not required if N provided)", type=int)
rsa_parser.add_argument("--min", help="Minimum prime value for key generation", type=int)
rsa_parser.add_argument("--max", help="Maximum prime value for key generation", type=int)

# elgamal
elgamal_parser = individual_cipher_arg_parsers.add_parser("elgamal", help="RSA Cipher")
elgamal_parser.add_argument("-t", "-t1","--text", "--text1", required=True, help="Text to encrypt", type=int)
elgamal_parser.add_argument("-t2","--text2", help="Text Km to decrypt (Decrypt/Crack)", type=int)
elgamal_parser.add_argument("-k", "--little-k", help="Little k/random number (Encrypt optional)", type=int)
elgamal_parser.add_argument("-y", "--receiver", help="Receiver's y value (Encrypt/Crack)", type=int)
elgamal_parser.add_argument("-b", "-x", "--private", help="Receiver's private key (Decrypt)", type=int)
elgamal_parser.add_argument("-a", "-r", "--root", required=True, help="Root value", type=int)
elgamal_parser.add_argument("-p", "--modulus", required=True, help="Modulus value", type=int)

# maassey-omura
massey_omura_parser = individual_cipher_arg_parsers.add_parser("massey", help="Massey-Omura cryptosystem")
massey_omura_parser.add_argument("-t","--text", required=True, help="*Number to encrypt/decrypt")
massey_omura_parser.add_argument("-p", "--prime", required=True, help="Prime number")
massey_omura_parser.add_argument("-a", "-s", "--sender", help="Sender/Alice's key")
massey_omura_parser.add_argument("-b", "-r","--receiver", help="Receiver/Bob's key")
massey_omura_parser.add_argument("-1", "--step1", help="m^sender - used by crack")
massey_omura_parser.add_argument("-2", "--step2", help="m^(sender*receiver) - used by crack")
massey_omura_parser.add_argument("-3", "--step3", help="m^receiver - used by crack")

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
        case "caesar":
            call_caesar(prog_args)
        case "simple":
            call_simple_substitution(prog_args)
        case "feistel":
            call_feistel(prog_args)
        case "elgamal":
            call_elgamal(prog_args)
        case "massey":
            call_massey_omura(prog_args)
        case "rsa":
            call_rsa(prog_args)
        case _:
            print("Unsupported cipher type:", prog_args.cipher)
            sys.exit(1)
                

if __name__ == "__main__":
    main()
