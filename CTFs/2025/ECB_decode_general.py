#!/usr/bin/env python3
import os
import sys
import binascii
from math import ceil
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

BLOCK_SIZE = 16

flag_size = 24
FLAG_PATH = "./longflag.txt"

ASCII_RANGE = list(range(33,127)) # hex 21 (!) to (and include) hex 7e (~)

try:
	with open(FLAG_PATH, "rb") as f:
		FLAG = f.read().strip()
except FileNotFoundError:
	print(f"[!] {FLAG_PATH} missing — create the file with your real flag.")
	sys.exit(1)

KEY = os.urandom(16)
print(f"key is {KEY} ... shhh....")

def encrypt_oracle(user_bytes: bytes) -> bytes:
	plaintext = user_bytes + FLAG
	padded = pad(plaintext, BLOCK_SIZE)
	print(padded.decode())
	cipher = AES.new(KEY, AES.MODE_ECB)
	return cipher.encrypt(padded)


def guess_decrypt(guess,padding):
	padding_val = 16*ceil(len(guess)/16) - len(guess)
	print(f"\tpadding_val: {padding_val}, length: {padding}")
	pt = guess + padding_val.to_bytes(1,'little')*padding
	ct = encrypt_oracle(pt)
	return ct
	
decrypted_flag = b''
for size in range(1,flag_size+1): #(1 - 24)
	print(f'\t{size}:\n')
	padding = 16 + 16*ceil(size/16)-size #(16+nearest mult of 16-len(guess) 
	for i in ASCII_RANGE:
		guess = i.to_bytes(1,'little') + decrypted_flag 
		#print(f"guess: {guess}")
		result = guess_decrypt(guess,padding)	
		compare_range = 16*ceil(len(guess)/16) #round up to nearest mult of 16
		if result[:compare_range] == result[-compare_range:]:
			print(guess)
			decrypted_flag = i.to_bytes(1,'little') + decrypted_flag
			break # early break

print(decrypted_flag)
