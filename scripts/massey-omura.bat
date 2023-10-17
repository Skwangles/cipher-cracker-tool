@echo off
echo #### Encrypt ####
python main.py --encrypt massey -t 3 -p 17 -a 11 -b 7

echo #### Decrypt ####
python main.py --decrypt massey -t 11 -p 17 -a 11 -b 7

echo #### Crack ####
python main.py --crack massey -p 17 -1 7 -2 12 -3 11

