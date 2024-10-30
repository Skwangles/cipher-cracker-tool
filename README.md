# Group Project - Encrypter, Decrypter and Cracker Tool
## Ciphers implemented

- Caesar cypher - Smart crack;
- Simple Substitution - Quadgram Hill climb and frequency analysis;
- Vigenere cypher - Period analysis;
- Feistel cypher (No Crack);
- Massey-Omura;
- R.S.A. - FactorDB, Fermat's Factorization, and Brute force from primes saved in txt file;
- ElGamal 

## How to use

_Note: You must be running atleast Python 3.10 - otherwise the 'match' statements will throw syntax errors_  

Install libraries:  
`pip install -r requirements.txt`

```
usage: main.py [-h] [--encrypt] [--decrypt] [--crack] [--generate] {caesar,rsa,elgamal,massey,simple,feistel,vigenere} ...

Encrypt, decrypt or crack a cipher text.

options:
  -h, --help            show this help message and exit

cipher:
  {caesar,rsa,elgamal,massey,simple,feistel,vigenere}
                        Cipher types - rsa, caesar, simple, feistel
    caesar              Caesar Cipher
    rsa                 RSA Cipher
    elgamal             El Gamal Cryptosystem
    massey              Massey-Omura cryptosystem
    simple              Simple Substitution Cipher
    feistel             Feistel Cipher
    vigenere            Vigenere Cipher

action:
  --encrypt, -e         Encrypt the plain text
  --decrypt, -d         Decrypt the cipher text
  --crack, -c           Crack the cipher text
  --generate, -g        Generate a key
```

Current system usage:  
`python main.py -h`

Feistel Cipher example:  
`python main.py --encrypt feistel -t test -k abc -r 10`

Caesar Cipher example:  
`python main.py --encrypt caesar -t test -s 3`

Simple Cipher example:  
`python main.py --encrypt simple -t -k abcdefghijklmnopqrstuv` (Key must be 26 letters)

Vigenere Cipher example:  
`python main.py --encrypt vigenere -t test -k cars`

RSA Cipher example:  
`python main.py  --encrypt rsa -t 95 -n 58687709 -e 270679`

Massey Omura Cipher example:  
`python main.py --encrypt massey -t 104 -p 3433 -a 1697 -b 31`

El Gamal Cipher example:  
`python main.py  --encrypt elgamal -t 42 -k 1343 -y 1828 -a 30 -p 13757`

