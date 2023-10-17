@echo off

echo #### Encrypt ####
python main.py --encrypt vigenere -t "Hello World this is your captain speaking i would like to warn you of dangerous water that lie ahead please be mindful of the evil that lies in the mist as it can kill those unwary" -k "abc"

echo #### Decrypt ####
python main.py --decrypt vigenere -t "HFNLP YOSND UJIT KS ZQUS EAQVAJP SQGALKNH K WPWLE NILG TP YASP YPW OG FAOIESQUT YAUGR UJAU NIF CHFCD QNEBUE CG MJPDGWL PH TIG EWKL UJAU NIFU IO VHF OITV AT KT DCN LKLM VHPUE VPWBTY" -k "abc"

echo #### Crack ####
python main.py --crack vigenere -t "HFNLP YOSND UJIT KS ZQUS EAQVAJP SQGALKNH K WPWLE NILG TP YASP YPW OG FAOIESQUT YAUGR UJAU NIF CHFCD QNEBUE CG MJPDGWL PH TIG EWKL UJAU NIFU IO VHF OITV AT KT DCN LKLM VHPUE VPWBTY" 