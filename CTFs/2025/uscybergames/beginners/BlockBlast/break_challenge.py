#!/usr/bin/env python3
import os
import sys
import socket
import time
from math import ceil
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

#flag_size = 9
flag_size = 25 # add another block: (9 + 16)
BLOCK_SIZE = 16

def clean_hex(hexin):
	"""mainly to strip the mysterious ">" char that appears, probably from the prompt. Bonus: removes whitespace"""
	clean = ""
	allowed = '0123456789abcdef'
	for h in hexin:
		if h in allowed:
			clean += h
	return clean

ASCII_RANGE = list(range(33,127)) # hex 21 (!) to (and including) hex 7e (~)

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


KEY = os.urandom(16)


host = "challenge.ctf.uscybergames.com"
port = 49143


decrypted_flag = b''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	
	s.connect((host,port))

	s.sendall('aa\n'.encode())
	response = s.recv(4096).decode()


	for flag in range(1,flag_size+1): #(2 - 24)
		padding_size = (top_block(flag_size)-flag_size) + 16
		for i in ASCII_RANGE:
			guess = i.to_bytes(1,'little') + decrypted_flag
			padding_val = get_padding_val(len(guess))
			pt = guess + padding_val.to_bytes(1,'little')*padding_size
			pt = pt.hex()
			#print("starting:", pt,type(pt))
			compare_range = 2*top_block(len(guess)) # determines how many bytes to compare

			send = pt.encode('utf-8')+b'\n'
			#print(f"Sending: {pt}")
			s.sendall(send)
			response = s.recv(4096)
			#print(f"Received {len(response)} bytes")
			#print("Response hex:", response.decode())
			ct = response.decode() #(response.decode()).strip()
			ct = clean_hex(ct)
		
			if ct[:compare_range] == ct[-compare_range:]:
				decrypted_flag = i.to_bytes(1,'little') + decrypted_flag
				print(decrypted_flag)
				break
	print(decrypted_flag)
