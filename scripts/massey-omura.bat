@echo off
echo #### Encrypt ####
python main.py --encrypt massey -t 104 -p 3433 -a 1697 -b 31

echo #### Decrypt ####
python main.py --decrypt massey -t 132 -p 3433 -b 31

echo #### Crack ####
python main.py --crack massey -1 3157 -2 2164 -3 132 -p 3433

