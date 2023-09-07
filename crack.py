def crack(args):
    if len(args) != 2:
        print_help()
        return
    print(args)
    match args[0].lower():
        case "rsa":
          # insert calls to RSA cracker, etc
          break
        case "c":
          # insert calls to Caesar cipher cracker, etc
          break
        case "ss":
          # insert calls to Simple Substitution cracker, etc
          break
        # Insert whatever extra ciphers we choose here
        case _:
          print("Not a supported cipher type")
          print_help()


def encrypt(args):
  if len(args) != 3:
        print_help()
        return
    
    match args[0].lower():
        case "rsa":
          # insert calls to RSA cracker, etc
          break
        case "c":
          # insert calls to Caesar cipher cracker, etc
          break
        case "ss":
          # insert calls to Simple Substitution cracker, etc
          break
        # Insert whatever extra ciphers we choose here
        case _:
          print("Not a supported cipher type")
          print_help()


def decrypt(type, text, key):
   if len(args) != 3:
        print_help()
        return
     
    match args[0].lower():
        case "rsa":
          # insert calls to RSA cracker, etc
          break
        case "c":
          # insert calls to Caesar cipher cracker, etc
          break
        case "ss":
          # insert calls to Simple Substitution cracker, etc
          break
        # Insert whatever extra ciphers we choose here
        case _:
          print("Not a supported cipher type")
          print_help()
  

def print_help():
  print("Usage: python crack.py <c-crack|e-encrypt|d-decrypt> <cipher-type> <ciphertext>")
  print("""
        Cipher type options: 
          RSA - RSA encryption, 
          C - Caesar Cipher 
          SS - Simple Substitution
        
        e.g. python crack.py c ss abcdefg
        """)
            
if __name == "__main__":
    args = sys.argv
    # Verify args
    if len(args) <= 1:
      print_help()
      print("Please provide one or more arguments.")
      return
      
    # Determine operation  
    match args[1].lower():
        case "e":
          encrypt(args[2:])
        case "d":
          decrypt(args[2:])
        case "c":
          crack(args[2:])
    
      
