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
import matplotlib.pyplot as plt
import math
import numpy as np
import shutil
import string

regenerate = False # flag for determining whether or not to redo the longer steps (such as calculating monogram or tetragram frequencies

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
	total_chars = 0
	for char in monograms:
		total_chars+= monograms[char]

	for char in monograms:
		monograms[char] = monograms[char]/total_chars

	return monograms

# task 2
"""
Use your function in a script to take your corpus and compile the frequencies of each letter. Do not include spaces as a letter. Your script should store the frequency table in a format that you can read and understand later.
"""

loaded_corpus = ''
with open(dst) as f:
	for line in f:
		loaded_corpus += line

monogram_freq = monogram_frequency(loaded_corpus)

monogram_freq_nospaces_file = "monogram_freq.json"
shutil.rmtree(monogram_freq_nospaces_file, ignore_errors=True)
with open(monogram_freq_nospaces_file, 'w') as f:
	json.dump(monogram_freq, f)


# task 3
"""
Use your function in a script to compile a table of monogram frequencies that includes spaces. Remember that newline characters separate words, so they should count as spaces. Store the table in a format that you can read and use later.
"""

monogram_freq_spaces = monogram_frequency(loaded_corpus, include_space=True)
monogram_frequency_file = "monogram_freq_spaces.json"
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


def make_tetragram_freq(loaded_corpus, include_spaces=False):
	allowed = string.ascii_uppercase
	if include_spaces:
		allowed += ' '
	upper_src = ' '.join(loaded_corpus.upper().split()) # split on new lines, tabs, etc. then rejoin
	upper_src = upper_src.replace('-',' ')
	one_string =  ''.join([c for c in list(upper_src) if c in allowed])

	# create and return tetragrams - all possible 4 char permutations
	all_perms = [''.join(p) for p in itertools.product(allowed,repeat=4)]
	tetragrams = dict(zip(all_perms,[0]*len(all_perms)))
	for i in range(len(one_string)-3): # -3 to ensure we stop at final tetra val
		tetra = one_string[i:i+4]
		tetragrams[tetra] += 1
	tetragrams = dict(sorted(tetragrams.items(), key=lambda d: d[1], reverse=True))
	count = 0
	# get frequencies
	for tetra in tetragrams:
		count += tetragrams[tetra]
	for tetra in tetragrams:
		tetragrams[tetra] /= count
	return dict(tetragrams)
	

#print(make_tetragram_freq(loaded_corpus))
#print(make_tetragram_freq(loaded_corpus, include_spaces=True))

# task 3
"""
Write another script to take your tables and create two new tables. In the new tables, each frequency is replaced with its logarithm. Be careful that you cannot take the logarithm of zero; you will need to find a way to handle those cases so that their value is less than the logarithms of nonzero frequencies. Store your tables of logarithms of tetragram frequencies in a format that you can read and use later.
"""

def log_freq(ngram,base=10):
	for n in ngram:	
		try:
			ngram[n] = math.log(ngram[n],base)
		except ValueError:
			ngram[n] = -math.inf
	return ngram

log_freq_file_nospaces = 'tetragram_log_frequency_nospaces.json'
if regenerate:
	log_freq_nospaces = log_freq(make_tetragram_freq(loaded_corpus))
	shutil.rmtree(log_freq_file_nospaces,ignore_errors=True)
	with open(log_freq_file_nospaces,'w') as f:
		json.dump(log_freq_nospaces, f, indent=4)


log_freq_file_spaces = 'tetragram_log_frequency_spaces.json'
if regenerate:
	log_freq_spaces = log_freq(make_tetragram_freq(loaded_corpus,include_spaces=True))
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
#keys = list(log_freqs.keys())
#for k in keys[:10]:
#	print(f'{k}: {log_freqs[k]}')


# Unit 7 - the chi-squared statistic

def chi_square_test(vals, exp_vals):
	total = 0
	for i in range(len(vals)):
		total += ((vals[i] - exp_vals[i])**2)/exp_vals[i]

	return total

# exercise
#chi_square =  chi_square_test([1.1,2.5,7.3],[1,3,7])
#print(chi_square)


# Unit 8 - monogram fitness with the chi-squared statistic

# Task 1
"""
Write a function that calculates the fitness of a piece of text by comparing its monogram frequencies to those of English. Use the functions that you previously wrote for finding the monogram frequencies of a text and for calculating the χ2 statistic. Remember that since the χ2 statistic is small for a good fit, you should either negate the result or take its reciprocal when defining the fitness. The frequencies that you found from your corpus take the role of the expected values when doing the calculation. Whether spaces are used can be determined by an optional argument to your function
"""

def chi_square_fitness_mono(sample_freq, eng_freq, spaces=False):
	sample = sample_freq.copy()
	if not spaces:
		sample.pop(" ",None)
	vals = []
	exp_vals = []
	exp_vals
	for l in sample.keys():
		vals.append(sample[l])
		exp_vals.append(eng_freq[l])
	return chi_square_test(vals,exp_vals)


# exercise 1
"""
 For various lengths, take several randomly chosen passages of each length from your corpus (or any other texts) and find the fitness of each. Make a graph of the fitness as a function of the length of  the selected text. From your graph, notice the variability in the fitness and how it depends on the  length of text.
"""

lengths = list(range(100,1000,100))
chi_squared_vals = []

section = ""
for i in range(1,10):
	start = i*len(loaded_corpus)//10
	section += loaded_corpus[start:start+500]
	sample_monogram = monogram_frequency(section)
	chi = chi_square_fitness_mono(sample_monogram,monogram_freq_spaces)
	#print(section)
	#print(chi)
	#print()
	chi_squared_vals.append(chi)

#plt.scatter(lengths,chi_squared_vals)
#plt.title("χ2 statistic as a function of sample size")
#plt.show()

# Unit 9 - Angle between vectors
"""
1. Write a function that finds the inner product of two vectors. You can represent vectors as lists or tuples. The dimension of the vectors can be found with the len() function. If the dimensions of the two vectors do not match, the function should throw and exception, raise an error, or somesuch.
2. Write a function that returns the cosine of the angle between two vectors
"""
def inner_product(u,v):
	try:
		product = np.dot(u,v)
	except Exception as e:
		print(e)
	return product

def cos_angle(u,v):
	num = inner_product(u,v)
	denom = np.sqrt(inner_product(u,u)*inner_product(v,v))
	return num/denom

#u = [1,2,3]
#v = [2,4,6]
#angle = cos_angle(u,v)
#print(angle)

# Unit 10 - monogram fitness with angle between vectors

def monogram_cos_fitness(sample_monograms, corpus_monograms,spaces=False):
	sample_copy = sample_monograms.copy()
	if not spaces:
		try:
			sample_copy.pop(' ')
		except:
			pass

	sample = []
	source = []
	for k in sample_copy.keys():
		sample.append(sample_copy[k])
		source.append(corpus_monograms[k])

	cos_fitness = cos_angle(sample,source)
	return cos_fitness



"""
For various lengths, take several randomly chosen passages of each length from your corpus (or any other texts) and find the fitness of each. Make a graph of the fitness as a function of the length of the selected text. From your graph, notice the variability in the fitness and how it depends on the length of text.
"""
#lengths = list(range(100,1000,100))
#cos_fitness_vals = []

#section = ""
#for i in range(1,10):
#	start = i*len(loaded_corpus)//10
#	section += loaded_corpus[start:start+500]
#	sample_monogram_frequency = monogram_frequency(section)
#	sample_cos_fitness = monogram_cos_fitness(sample_monogram_frequency, monogram_freq_spaces)
#	cos_fitness_vals.append(sample_cos_fitness)
#plt.scatter(lengths, cos_fitness_vals)
#plt.title("cosine fitness as a function of sample size")
#plt.show()

# Unit 11 - Tetragram fitness
"""
 Write a function that calculates the tetragram fitness of a piece of text. It should use your table of logarithms of tetragram frequencies. Since you only want to read the table into memory once, you should use the function you wrote in Unit 4 for that purpose before you call the fitness function. Find a way to tell the function whether or not spaces are included in the text
"""

def tetragram_fitness(sample,spaces=False):
	""" assumes everything has been cleaned. Maybe go back and add cleaning feature for "Regular text" """
	sample_copy = sample
	if spaces:
		freq_file = 'tetragram_log_frequency_spaces.json'
	else:
		sample_copy = ''.join(sample.split())
		freq_file = 'tetragram_log_frequency_nospaces.json'
	L = len(sample_copy)
	log_freq = load_log_frequencies(freq_file)
	sample_tetragrams = [sample_copy[i:i+4] for i in range(len(sample_copy)-3)]
	log_sum = 0
	for tetra in sample_tetragrams:
		log_sum += log_freq[tetra]
	return log_sum/(L-3)


lengths = list(range(100,1000,100))
tetragram_fitness_vals = []

section = ""
for i in range(1,10):
   start = i*len(loaded_corpus)//10
   section += loaded_corpus[start:start+500]
   sample_tetragram_fitness = tetragram_fitness(section)
   tetragram_fitness_vals.append(sample_tetragram_fitness)

print(lengths)
print(tetragram_fitness_vals)
plt.scatter(lengths, tetragram_fitness_vals)
plt.title("tetragram fitness as a function of sample size")
plt.show()
