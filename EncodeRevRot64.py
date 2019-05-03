#!/usr/bin/env python3

# I made this for a puzzle on my 30th birthday, 
# can be useful for encoding other stuff I guess..

import os
import codecs
import base64


input("The purpose of this is program is to encrypt a file of your choice by" \
	" \nreversing the text, performing ROT13, then base64 encoding the result" \
	" \nPress <enter> to continue")

print ("Here are the files in the current directory: \n\n")


for r,d,f in os.walk(".",topdown=False):
	pass

			# Lessons learned:
			# "topdown = False" necessary to get current directory
			# otherwise it only gathers the deepest data
			# i.e. it would list the contents in the last directory
			# and any of its last subdirectories and so on


for i in f:
	print (i)

document = input ("\nWhich file do you want me to encode?  ")

print("\n\n")

while document not in f:
	document = input("\n I'm sorry, that file isn't in the current directory," \
						"\nplease provide a valid input: ")

with open(document,'r') as doc:
	line = doc.read()
	lineback = line[::-1]
	linerot = codecs.encode(lineback,"rot13")
	command = "echo "+'"'+linerot+'"'+" >> BackThenRot.txt"
	os.system(command)

os.system("base64 BackThenRot.txt")

os.system("rm -f BackThenRot.txt")

print("\n\n\ndone!")
