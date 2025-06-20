#!/usr/bin/env python3
""" an ECB cipher breaker. Determines the last byte one at a time by mimicking the padding pattern given the block size. In this case, the flag or hidden message is prepended to any input/guess. Provided the output is returned, the size of the message (flag_size in this example) can be determined and then the deciphering can take place from there"""
import os
import sys
from math import ceil
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

BLOCK_SIZE = 16

#FLAG_PATH = "./longflag.txt"
#flag_size = 24

#FLAG_PATH = "./shortflag.txt"
#flag_size = 11

#FLAG_PATH = "./flag.txt"
#flag_size = 16
FLAG_PATH = "./newflag.txt"
flag_size = 25

ASCII_RANGE = list(range(33,127)) # hex 21 (!) to (and including) hex 7e (~)

try:
	with open(FLAG_PATH, "rb") as f:
		FLAG = f.read().strip()
except FileNotFoundError:
	print(f"[!] {FLAG_PATH} missing — create the file with your real flag.")
	sys.exit(1)

#FLAG = bytes("abcdefghi",'utf-8')
#flag_size = 9


KEY = os.urandom(16)
print(f"key is {KEY} ... shhh....")

def print_blocks(val):
	print("vvvvvvvvv")
	for i,v in enumerate(val):
		print(f'{hex(int(v))[2:].zfill(2)}',end="")
		if i%16 == 0:
			print()
	print("\n^^^^^^^^^")

def top_block(val):
	""" helper: rounds up to nearest multiple of blocksize 	
		eg. 15 -> 16,  24 -> 32"""
	if val%16 == 0:    # round 16 -> 32, 32 -> 48 etc. to account for final padding
		return val + 16
	return BLOCK_SIZE*ceil(val/BLOCK_SIZE)

def get_padding_val(guess_size):
	if guess_size % 16 == 0:
		return 16
	return top_block(guess_size) - guess_size


def encrypt_oracle(user_bytes: bytes) -> bytes:
	plaintext = user_bytes + FLAG
	padded = pad(plaintext, BLOCK_SIZE)
	#print(padded.decode())
	cipher = AES.new(KEY, AES.MODE_ECB)
	return cipher.encrypt(padded)


def guess_decrypt(guess,padding_size):
	padding_val = get_padding_val(len(guess))
	pt = guess + padding_val.to_bytes(1,'little')*padding_size
	ct = encrypt_oracle(pt)
	return ct
	

def breaker():
    decrypted_flag = b''
    for size in range(1,flag_size+1): #(1 - 24)
        padding_size = (top_block(flag_size)-flag_size) + 16
        for i in ASCII_RANGE:
            guess = i.to_bytes(1,'little') + decrypted_flag
            result = guess_decrypt(guess,padding_size)
            compare_range = top_block(len(guess)) # determines how many bytes to compare
            if result[:compare_range] == result[-compare_range:]:
                print(guess)
                decrypted_flag = i.to_bytes(1,'little') + decrypted_flag
                break # early break

    print(decrypted_flag)

breaker()
"""decrypted_flag = b''
for size in range(1,flag_size+1): #(1 - 24)
	padding_size = (top_block(flag_size)-flag_size) + 16 
	for i in ASCII_RANGE:
		guess = i.to_bytes(1,'little') + decrypted_flag
		result = guess_decrypt(guess,padding_size)	
		compare_range = top_block(len(guess)) # determines how many bytes to compare
		if result[:compare_range] == result[-compare_range:]:
			print(guess)
			decrypted_flag = i.to_bytes(1,'little') + decrypted_flag
			break # early break

print(decrypted_flag)"""
