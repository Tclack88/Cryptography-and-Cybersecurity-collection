from fpdf import FPDF
from hashlib import md5
import itertools
import re
import sys
import os
 
letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

collisions = []
guesses = []
for i in range(8):
    for guess in itertools.product(letters, repeat=i):
        guess = ''.join(guess)
        checksum = md5(guess.encode()).hexdigest()
        if re.match(r'0e\d+\b',checksum):
            collisions.append(checksum)
            guesses.append(guess)
            print(guess, checksum)
            if len(collisions) > 2:
                sys.exit(0)
