@echo off

echo #### Encrypt ####
python main.py  --encrypt rsa -t 42 -n 37344221 -e 11

echo #### Decrypt ####
python main.py  --decrypt rsa -t 27395919 -n 37344221 -d 16969091

echo #### Crack ####
python main.py --crack rsa -t 27395919 -n 37344221 -e 11

echo #### Generate Weak Key  (p, q, d, e, n) ####
python main.py  --generate rsa --min 1000 --max 10000

