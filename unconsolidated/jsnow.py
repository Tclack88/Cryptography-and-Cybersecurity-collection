#!/usr/bin/env python3

# the purpose of this program is to brute force an etc/shadow password hash for an example user
# In this case, the user is jsnow. This is used in conjunction with the .txt file:
# potentialpasswords.txt, a text file containing all possible words greater than 6 characters
# this limitation stems from a 6-character password minimum on the server
# This takes about 1300 seconds to find the appropriate password

import os
import crypt
import time


os.system('grep ...... words.txt > potentialpasswords.txt')
#CSIL servers require 6 char minimum for passwords, so this reduces the
#potential passwords to save time

passfile = 'potentialpasswords.txt'

#jsnow 
hashed = "$6$aBcDeF$qn4wyWpQKwjaKGr02tGUWKcFjl0p90b68.oaaJTFX87UzsSWIzq3ZoAEG0/xUQ1kcYTiHkKqye1Qat6vL4rMZ."
salt = '$6$aBcDeF$'




time_start = time.perf_counter()

with open(passfile) as f0:
    for line in f0:
        password = line[0:-1]   # need -1 perhaps to rm newline char?
        output = crypt.crypt(password,salt)
        print(line,output)
        if output == hashed:
            print("password is:",password)
            print(":]\n:]\n:]")
            time_end = time.perf_counter()
            print('total time:',time_end-time_start)
            exit(0)



