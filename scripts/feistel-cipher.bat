@echo off
echo #### Encrypt ####
python main.py --encrypt feistel -t "Hello World This is your captain speaking i would like to warn you of dangerous waters that lie ahead" -k "abc" -r 16 

echo #### Decrypt ####
python main.py --decrypt feistel -t "bb97e7060155c1583d432daa64c9f24b17fe261a0946fc33407af74e20537f41574e64600346da4c4842cfd0485303d10409497c2b00e0e1da20f7d1876e35b93f5025aa467071514b0290e70a55436572f461a5d71375e1887141a5d959c055e4388044f4" -k "abc" -r 16