@echo off
echo #### Encrypt ####
python main.py --encrypt massey -t 42 -p 61 -a 3 -b 8 -1 22 -2 44 -3 13

echo #### Decrypt ####
python main.py --decrypt -t 22 -p 61 -a 3 -b 8 --step1 22 --step2 44 --step3 13

echo #### Crack ####
python main.py --crack massey -t 22 -p 61 -a 3 -b 8

