@echo off

echo #### Encrypt ####
python main.py  --encrypt elgamal -t 13 -k 3 -y 8 -a 5 -p 23

echo #### Decrypt ####
python main.py --decrypt elgamal -t 10 -t2 9 -b 6 -a 5 -p 23

echo #### Crack ####
python main.py --crack elgamal -t 10 -t2 9 -y 8 -a 5 -p 23 --crack-b