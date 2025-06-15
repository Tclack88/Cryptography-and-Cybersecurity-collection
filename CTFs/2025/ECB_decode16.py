#!/usr/bin/env python3
""" An implementation of breaking ECB (electronic code block) decrypting one byte at a time"""
import os
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

BLOCK_SIZE = 16
FLAG_PATH = "./flag.txt"

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
	cipher = AES.new(KEY, AES.MODE_ECB)
	return cipher.encrypt(padded)


def guess_decrypt(guess,padding):
	pt = guess + padding.to_bytes(1,'little')*16
	ct = encrypt_oracle(pt)
	return ct
		
padding = 16
decrypted_flag = b''
while padding >= 0:
	for i in ASCII_RANGE:
		guess = i.to_bytes(1,'little') + decrypted_flag 
		result = guess_decrypt(guess,padding)	
		if result[:16] == result[-16:]:
			decrypted_flag = i.to_bytes(1,'little') + decrypted_flag
			print(decrypted_flag)
			break # early break?
	padding -= 1

print(decrypted_flag)
