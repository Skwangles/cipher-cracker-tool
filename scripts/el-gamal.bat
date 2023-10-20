@echo off

echo #### Encrypt ####
python main.py  --encrypt elgamal -t 42 -k 1343 -y 1828 -a 30 -p 13757

echo #### Decrypt ####
python main.py --decrypt elgamal -t 8339 -t2 4519 -b 9742 -a 30 -p 13757

echo #### Crack ####
python main.py --crack elgamal -t 12380 -t2 3833 -y 1828 -a 30 -p 13757