# cipherchallenge.org
# Unit 1

# Task1
"""
Compile a corpus of English text. Be sure to remove all cover pages, licenses, tables of contents, etc., and diacritical marks (accent marks).
"""

# Task2 	
"""
Take your corpus and create another one that contains no punctuation. Be careful of hyphens at the ends of lines; they might be in the middle of words. Your finished corpus should contain only words separated by single spaces (or end-of-line characters). Feel free to convert all letters to upper-case or to lower-case.
"""
import fileinput
import shutil

src = "alice_in_wonderland.txt"
dst = "eng_corpus.txt"
shutil.copyfile(src,dst)

with fileinput.input(files=dst, inplace=True) as f:
	for line in f:
		line = ''.join([l for l in line if l.isalpha() or l==' ']).lower()
		print(line,end=' ')


	
