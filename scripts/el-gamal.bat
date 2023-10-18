@echo off

echo #### Encrypt ####
python main.py  --encrypt elgamal -t 100 -k 13442 -y 1828 -a 30 -p 13757

echo #### Decrypt ####
python main.py --decrypt elgamal -t 12380 -t2 3833 -b 9742 -a 30 -p 13757

echo #### Crack ####
python main.py --crack elgamal -t 12380 -t2 3833 -y 1828 -a 30 -p 13757