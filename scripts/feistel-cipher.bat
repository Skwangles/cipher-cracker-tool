@echo off
echo #### Encrypt ####
python main.py --encrypt feistel -t "My mama always said life was like a box of chocolates." -k "forrest-gump" -r 16 

echo #### Decrypt ####
python main.py --decrypt feistel -t "6f7e1b94c4e60e484c0531fa921ab726513ad5b162f4cb1106403463357cec0bd0f044b0672a9dd0da33d0567d5f639a0cc114d583" -k "forrest-gump" -r 16