import sys

# Cipher modules
import caesar_cipher
import rsa
import simple_substitution
import feistal_cipher

### --- Cipher calls
def call_rsa(args):
    match args[0].lower():
        case "crack":
            print(rsa.crack(args[1]))
        case "decrypt":
            print(rsa.decrypt(args[1], args[2]))
        case "encrypt":
            print(rsa.encrypt(args[1], args[2]))
        case _:
            print("Unsupported operation:", args[0])
            print_help()

def call_caesar_cipher(args):
    match args[0].lower():
        case "crack":
            print(caesar_cipher.crack(args[1]))
        case "decrypt":
            print(caesar_cipher.decrypt(args[1], args[2]))
        case "encrypt":
            print(caesar_cipher.encrypt(args[1], args[2]))
        case _:
            print("Unsupported operation:", args[0])
            print_help()

def call_simple_substitution(args):
    match args[0].lower():
        case "crack":
            print(simple_substitution.crack(args[1]))
        case "decrypt":
            print(simple_substitution.decrypt(args[1], args[2]))
        case "encrypt":
            print(simple_substitution.encrypt(args[1], args[2]))
        case _:
            print("Unsupported operation:", args[0])
            print_help()

def call_fiestal_cipher(args):
    match args[0].lower():
        case "crack":
            print(feistal_cipher.crack(args[1]))
        case "decrypt":
            print(feistal_cipher.decrypt(args[1], args[2], args[3], args[4]))
        case "encrypt":
            print(feistal_cipher.encrypt(args[1], args[2], args[3], args[4]))
        case _:
            print("Unsupported operation:", args[0])
            print_help()
            
### ----- General functions -----

def print_help():
    print("Usage: python main.py <cipher-type> <crack|encrypt|decrypt> <ciphertext>")
    print("""
        Cipher type options: 
          rsa - RSA encryption, 
          caesar - Caesar Cipher 
          simple - Simple Substitution
          fiestal - Fietsal Cipher
        e.g. python main.py simple crack abcdefg
        """)


def main():
    prog_args = sys.argv
    # Verify args
    if len(prog_args) <= 1:
        print_help()
        print("Please provide one or more arguments.")
        return

    match prog_args[1].lower():
        case "rsa":
            call_rsa(prog_args[2:])
        case "caesar":
            call_caesar_cipher(prog_args[2:])
        case "simple":
            call_simple_substitution(prog_args[2:])
        case "feistal":
            call_fiestal_cipher(prog_args[2:])
        # Insert whatever extra ciphers we choose here
        case _:
            print("Not a supported cipher type")
            print_help()


if __name__ == "__main__":
    main()
