@echo off
echo #### Encrypt ####
python main.py --encrypt caesar -t "Hello, World!" -s 3

echo #### Decrypt ####
python main.py --decrypt caesar -t "Khoor, Zruog!" -s 3

echo #### Crack ####
python main.py --crack caesar -t "Khoor, Zruog!"
