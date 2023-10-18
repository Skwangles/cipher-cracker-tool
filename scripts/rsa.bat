@echo off

echo #### Encrypt ####
python main.py  --encrypt rsa -t 95 -n 58687709 -e 270679

echo #### Decrypt ####
python main.py  --decrypt rsa -t 37012695 -n 58687709 -d 5419

echo #### Crack ####
python main.py --crack rsa -t 41802438 -n 58687709 -e 270679

echo #### Crack - Fermats Factorization Method ####
python main.py --crack rsa -t 41802438 -n 88679873 -e 270679

echo #### Crack - Bruteforce ####
python main.py --crack rsa -t 41802438 -n 88679873 -e 270679