@echo off

echo #### Encrypt ####
python main.py  --encrypt rsa -t 100 -n 58687709 -e 270679

echo #### Decrypt ####
python main.py  --decrypt rsa -t 41802438 -n 58687709 -d 5419

echo #### Crack ####
python main.py --crack rsa -t 41802438 -n 58687709 -e 270679

