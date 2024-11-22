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
import json
import shutil
import string

src = "alice_in_wonderland.txt"
#src = "Jurassic_Park_eng.txt"
dst = "eng_corpus.txt"
shutil.copyfile(src,dst)

with fileinput.input(files=dst, inplace=True) as f:
	for line in f:
		line = ''.join([l for l in line if l.isalpha() or l==' ']).lower()
		print(line,end=' ')


# unit 2 - Word lists

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

# Task3
"""
Write a function that can read your ranked word list and put the words into a list or dictionary object for use by other functions.
"""

with open(word_count_file) as f:
	loaded_json = json.load(f)


# Unit 3 - Monogram Frequency Tables

"""
Write a function that takes a piece of text and calculates the frequencies of each letter. Allow for the possibility of either including spaces or excluding them (possibly with an optional parameter). End-of-line characters should count as a space.
"""

def monogram_frequency(text, include_space=False):
	"""
	Assumes the text has already been "cleaned"
	(removed non-alpha chars, lower case, newlines => " ", etc.) 
	"""
	monograms = {}
	allowed = string.ascii_lowercase
	if include_space:
		allowed += " "
	for t in text:
		if t in allowed:
			if monograms.get(t,None):
				monograms[t] += 1
			else:
				monograms[t] = 1

	monograms = sorted(monograms.items(), key=lambda w: w[1], reverse=True)
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
