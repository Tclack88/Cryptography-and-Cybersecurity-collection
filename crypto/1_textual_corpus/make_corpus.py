# cipherchallenge.org
# Unit 3

# Task1
"""
Compile a corpus of English text. Be sure to remove all cover pages, licenses, tables of contents, etc., and diacritical marks (accent marks).
"""

# Task2 	
"""
Take your corpus and create another one that contains no punctuation. Be careful of hyphens at the ends of lines; they might be in the middle of words. Your finished corpus should contain only words separated by single spaces (or end-of-line characters). Convert all letters to upper-case.
"""
import fileinput
import itertools
import json
import math
import shutil
import string

src = "alice_in_wonderland.txt"
#src = "Jurassic_Park_eng.txt"
dst = "eng_corpus.txt"
shutil.copyfile(src,dst)

with fileinput.input(files=dst, inplace=True) as f:
	for line in f:
		line = ''.join([l for l in line if l.isalpha() or l==' ']).upper()
		print(line,end=' ')


# Unit 4 - Word lists

# Task1
"""
Write a program that takes a text file and adds the words in it to a second file. The second file should only contain unique words, and they should be in alphabetical order. Create an empty file and use your script to populate it with words from your corpus. Your program will allow you to add more words to your list later, when you come across texts with unusual words or names.
"""

word_list = []
with open(dst,'r') as f:
	for line in f:
		word_list += line.split()

uniq_word_list = sorted(list(set(word_list)))

uniq_words_file = "uniq_words.txt"

shutil.rmtree(uniq_words_file,ignore_errors=True) # remove if exist for fresh start and avoid appending

with open(uniq_words_file, 'w') as f:
	f.write(' '.join(uniq_word_list))

# Task2
"""
Write a function to load your word list from the file that you created in Task 1 and creates a Python list for use by other functions.
"""

def load_wordlist(uniq_words_file):
	loaded_words = ""
	with open(uniq_words_file, 'r') as f:
		for line in f:
			loaded_words += line
		loaded_word_list = loaded_words.split()
	return loaded_word_list

#print(load_wordlist(uniq_words_file))



# Task3
"""
Write a program that takes a text file and adds word counts to a second file. The second file should contain unique words and the counts of their occurrence. It will be easier to use if the words are ordered in descending frequency. You can store the data in any way that you like (one word and number per line, or JSON, or ...), so long as you are able to read the information later. Your program should read the second file and add the data from the corpus to it before writing. Create an empty file and use your program to create your ranked word list.
"""

word_count = {}
for word in word_list:
	if word_count.get(word,None):
		word_count[word] += 1
	else:
		word_count[word] = 1

word_count =  dict(sorted(word_count.items(), key = lambda i: i[1],reverse=True))

word_count_file = 'word_count.json'
shutil.rmtree(word_count_file, ignore_errors=True)

with open(word_count_file,'w') as f:
	json.dump(word_count, f, indent=4)

# Task 4
"""
Write a function that can read your ranked word list and put the words into a list or dictionary object for use by other functions.
"""

with open(word_count_file) as f:
	loaded_json = json.load(f)


# Unit 5 - Monogram Frequency Tables

"""
Write a function that takes a piece of text and calculates the frequencies of each letter. Allow for the possibility of either including spaces or excluding them (possibly with an optional parameter). End-of-line characters should count as a space.
"""

def monogram_frequency(text, include_space=False):
	"""
	Assumes the text has already been "cleaned"
	(removed non-alpha chars, newlines => " ", etc.) 
	"""
	monograms = {}
	allowed = string.ascii_uppercase
	if include_space:
		allowed += " "
	for t in text:
		if t in allowed:
			if monograms.get(t,None):
				monograms[t] += 1
			else:
				monograms[t] = 1

	monograms = dict(sorted(monograms.items(), key=lambda w: w[1], reverse=True))
	return monograms

#sample = "hello! My name is Trevor, I'm super-duper happy to be here"
#monogram_freq = monogram_frequency(sample)
#print(monogram_freq)


# task 2
"""
Use your function in a script to take your corpus and compile the frequencies of each letter. Do not include spaces as a letter. Your script should store the frequency table in a format that you can read and understand later.
"""

src_text = ''
with open(src) as f:

	for line in f:
		src_text += line

monogram_freq = monogram_frequency(src_text)
#print(monogram_freq)


# task 3
"""
Use your function in a script to compile a table of monogram frequencies that includes spaces. Remember that newline characters separate words, so they should count as spaces. Store the table in a format that you can read and use later.
"""

monogram_freq_spaces = monogram_frequency(src_text, include_space=True)
monogram_frequency_file = "monogram_freq.json"
shutil.rmtree(monogram_frequency_file, ignore_errors=True)

with open(monogram_frequency_file, 'w') as f:
	json.dump(monogram_freq_spaces, f)


# task 4
"""
Write a function that can open the file(s) containing your monogram tables and put them into a list or dictionary object (or some other data type that you define), so that other functions can use them.
"""

def load_monogram_freq(monogram_frequency_file):
	with open(monogram_frequency_file,'r') as f:
		monogram_frequency_dict = json.load(f)
	return monogram_frequency_dict

#loaded_monogram_freq = load_monogram_freq(monogram_frequency_file)
#print(loaded_monogram_freq)

# Unit 6 - Tetragram frequency tables

# task 1/2
"""
1
Write a script to compile a table of tetragram frequencies from your corpus. Do not include spaces in this table. Your table will have 264  entries. Save the data in a format that you can access later.
2
Write a script to compile and save a table of tetragram frequencies that includes spaces. Remember that newline characters separate words, so they count as spaces.
"""


def make_tetragram_freq(src_text, include_spaces=False):
	allowed = string.ascii_uppercase
	if include_spaces:
		allowed += ' '
	upper_src = ' '.join(src_text.upper().split()) # split on new lines, tabs, etc. then rejoin
	upper_src = upper_src.replace('-',' ')
	one_string =  ''.join([c for c in list(upper_src) if c in allowed])

	# create and return tetragrams - all possible 4 char permutations
	all_perms = [''.join(p) for p in itertools.product(allowed,repeat=4)]
	tetragrams = dict(zip(all_perms,[0]*len(all_perms)))
	for i in range(len(one_string)-3): # -3 to ensure we stop at final tetra val
		tetra = one_string[i:i+4]
		tetragrams[tetra] += 1
	tetragrams = sorted(tetragrams.items(), key=lambda d: d[1], reverse=True)
	return dict(tetragrams)
	

#print(make_tetragram_freq(src_text))
#print(make_tetragram_freq(src_text, include_spaces=True))

# task 3
"""
Write another script to take your tables and create two new tables. In the new tables, each frequency is replaced with its logarithm. Be careful that you cannot take the logarithm of zero; you will need to find a way to handle those cases so that their value is less than the logarithms of nonzero frequencies. Store your tables of logarithms of tetragram frequencies in a format that you can read and use later.
"""

def log_freq(ngram,base=10):
	for n in ngram:
		try:
			ngram[n] = math.log(ngram[n],base)
		except ValueError:
			pass
	return ngram


log_freq_nospaces = log_freq(make_tetragram_freq(src_text))
log_freq_file_nospaces = 'tetragram_loq_frequency_nospaces.txt'
shutil.rmtree(log_freq_file_nospaces,ignore_errors=True)
with open(log_freq_file_nospaces,'w') as f:
	json.dump(log_freq_nospaces, f, indent=4)


log_freq_spaces = log_freq(make_tetragram_freq(src_text,include_spaces=True))
log_freq_file_spaces = 'tetragram_loq_frequency_spaces.txt'
shutil.rmtree(log_freq_file_spaces,ignore_errors=True)
with open(log_freq_file_spaces,'w') as f:
	json.dump(log_freq_spaces, f, indent=4)
	
# Task4
"""
Write a function (or two functions) to read your tables of logarithms of tetragram frequencies into some data object so that they can be used in a program/script.
"""

def load_log_frequencies(filename):
	with open(filename) as f:
		log_freq = json.load(f)
	return log_freq
		

log_freqs = load_log_frequencies(log_freq_file_nospaces)
print(log_freqs)
