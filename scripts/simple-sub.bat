@echo off
echo #### Encrypt ####
python main.py --encrypt simple -t "Hello everyone this is the king of the blue mountains speaking, and I want to steal your soul - why don't we all calm down a second and trust in the one who has set us free of this all the quick brown fox who jumps over the lazy dog!" -k "zyxwvutsrqponmlkjihgfedcba"

echo #### Decrypt ####
python main.py --decrypt simple -t "SVOOL VEVIBLMV GSRH RH GSV PRMT LU GSV YOFV NLFMGZRMH HKVZPRMT, ZMW R DZMG GL HGVZO BLFI HLFO - DSB WLM'G DV ZOO XZON WLDM Z HVXLMW ZMW GIFHG RM GSV LMV DSL SZH HVG FH UIVV LU GSRH ZOO GSV JFRXP YILDM ULC DSL QFNKH LEVI GSV OZAB WLT!" -k "zyxwvutsrqponmlkjihgfedcba"


echo #### Crack ####
python main.py --crack  simple -t "SVOOL VEVIBLMV GSRH RH GSV PRMT LU GSV YOFV NLFMGZRMH HKVZPRMT, ZMW R DZMG GL HGVZO BLFI HLFO - DSB WLM'G DV ZOO XZON WLDM Z HVXLMW ZMW GIFHG RM GSV LMV DSL SZH HVG FH UIVV LU GSRH ZOO GSV JFRXP YILDM ULC DSL QFNKH LEVI GSV OZAB WLT!"
