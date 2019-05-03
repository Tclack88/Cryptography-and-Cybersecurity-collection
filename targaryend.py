#!/usr/bin/env python3

# The purpose of this program is to brute force an etc/shadow hashed password
# The assumption is the password is alphanumeric and 6-8 characters long
# This took about 28000 seconds to complete

import itertools
import crypt
import time


hashed = 'aa.YVJDT1VruA'
salt = 'aa'

def BruteForce():
    
    time_begin = time.perf_counter()
    
    char_pool = 'abcdefghijklmnopqrstuvwxyz0123456789'
            # set a string of possible characters to draw from
    for password_length in range(6, 8):
        for guess in itertools.product(char_pool, repeat=password_length):
            # itertools is used for efficient looping. The product method gives
            # the cartesian product of the argument (the char_pool here)
            # process is repeat for 6 and 7 long character passwords

            guess = ''.join(guess)
            # ouput of itertools.product is a tuple, so it needs to be joined
            # into a coherent string
            output = crypt.crypt(guess,salt)
            print(guess,output)
            if output == hashed:
                time_end = time.perf_counter()
                total_time = time_end - time_begin
                print(total_time)
                exit(0)

BruteForce()
