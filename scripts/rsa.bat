@echo off

echo #### Encrypt ####
python main.py  --encrypt rsa -t 95 -n 58687709 -e 270679

echo #### Decrypt ####
python main.py  --decrypt rsa -t 37012695 -n 58687709 -d 5419

echo #### Crack ####
python main.py --crack rsa -t 41802438 -n 58687709 -e 270679 --factor-db

echo ### Generate Random Key (p, q, d, e, n) ###
python main.py --generate rsa --min 100 --max 10000

echo ### Generate Weak Key (p, q, d, e, n) - Close to together ###
python main.py --generate rsa --min 100 --max 10000 --weak

echo ### Crack weak key ###
python main.py --crack rsa -t 17690470 -n 69222319 -e 270679