import random
#from time import sleep
#import statistics
import sys

random.seed(1)

# based on https://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
eng_letters_ord = list('etaoinsrhdlucmfywgpbvkxqjz')
eng_let_freq_ord = [12.02,9.1,8.12,7.68,7.31,6.95,6.28,6.02,5.92,4.32,3.98,2.88,2.71,2.61,2.3,2.11,2.09,2.03,1.82,1.49,1.11,.69,.17,.11,.1,.07]
eng_freq = dict(zip(eng_letters_ord, eng_let_freq_ord))

#def calc_stdev(freq):
#	vals  = [val in freq.values()]
#stdev = statistics.pstdev(vals)

#print(eng_freq)
#sys.exit(0)
eng_ngrams = {}

def add_token(ngrams,start,l,i):
	sec = l[start:start + i]
	if ngrams.get(sec,None):
		ngrams[sec] += 1
	else:
		ngrams[sec] = 1
## Creating my own frequency list but using a "standard"
## one from a larger and probably broader english sample
#letter_count = {}
#
#def add_letter(l):
#	if letter_count.get(l,None):
#		letter_count[l] += 1
#	else:
#		letter_count[l] = 1
#		
#with open("Jurassic_Park_eng.txt",'r') as book:
#	for line in book:
#		line = ''.join([l.lower() for l in line if l.isalpha()])
#		for l in line:
#			add_letter(l)
#		
#print(letter_count)
#total = sum([val for val in letter_count.values()])
#print(total)
#for k,v in letter_count.items():
#	letter_count[k] = v/total*100
#
#
#
#print(sorted(letter_count.items(), key = lambda x: x[1], reverse=1))
#
#sys.exit(0)


def find_ngrams(list_list,ngrams):
        line_list = line.lower().split()
        for l in line_list:
            if not l.isalpha():
                l = ''.join([c for c in l if c.isalpha()])
            length = len(l)
            if length > 3:
                remaining = length
                start = 0
                while (remaining >= 3):
                    if remaining == 4:
                        add_token(ngrams,start,l,2)
                        start += 2
                        remaining -= 2
                        i = 2
                    elif remaining == 3:
                        i = 3
                    else:
                        i = random.choice([2,3])
                    add_token(ngrams,start,l,i)
                    start += i
                    remaining -= i
            else:
                start = 0
                add_token(ngrams,start,l,length)





with open ("Jurassic_Park_eng.txt",'r') as book:
	for line in book:
		find_ngrams(line, eng_ngrams)

eng_ngrams.pop('')
#for letter in 'bcdefghjklmnopqrstuvwxyz':
#	try:
#		tokens.pop(letter)
#	except KeyError:
#		continue

#print(len(eng_ngrams))

def normalize_dict(ngrams):
	for k,v in ngrams.items():
		ngrams[k] = v/len(ngrams)

normalize_dict(eng_ngrams)

#print(sorted(eng_ngrams.items(), key=lambda x: x[1], reverse=True))

# Phase 2: randomly vary english frequency list with adjacent
# letters, then translate and check against the n-grams
# created for the english language. A score is given from the
# n-grams. Higher score = more closely resembles English
# check against 100 or so random variations per round
# 
# implement a hill climbing algorithm with the top 10 scoring
# substitutions and vary, translate, repeat with the top 10 moving
# forward. Repeat many rounds (1000?) and choose the best scorer
# for the final translation

def translate(count_dict,eng_freq):
    # pass in dict count for content
    # and
    # frequency count for english letters
    # This will make direct translation from ciphered to english
    # frequency list provided

    #print(sorted(count_dict.items(), key=lambda x: x[1], reverse=True))
    mapper = {}

    for i,l in enumerate(count_dict):
        mapper[l[0]] = eng_freq[i]

    #print(mapper)

    substituted = ''

    for c in content:
        if mapper.get(c,None):
            substituted +=  mapper.get(c)
        else:
            substituted += c

    return substituted


def score_translation(substituted):
	content_ngrams = {}
	find_ngrams(substituted,content_ngrams)
	#print(sorted(content_ngrams.items(),key = lambda x : x[1], reverse=1))
	score = 0
	for k,v in content_ngrams.items():
		result = eng_ngrams.get(k,0)
		score += v*result
	return score

#def random_vary_translation():
#	# randomly swaps two adjacent letters in translation

content = ''
with open('subciph.txt') as f:
    for line in f:
        content+=line

content_list = [c for c in content if c.isalpha()]
count_dict = {}
for c in content_list:
    if count_dict.get(c,None) is not None:
        count_dict[c] += 1
    else:
            count_dict[c] = 1


substituted = translate(count_dict, eng_letters_ord)
score = score_translation(substituted)

print(score)
	





# Scoring: check against random 2-3 n grams of the content to be
# substituted with the english n-grams. If it appears, add that
# n gram frequency, if not present, add 0



#top_performers = {eng_freq}
