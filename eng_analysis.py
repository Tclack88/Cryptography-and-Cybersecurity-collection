import random
from time import sleep
import statistics
import sys

random.seed(1)

# based on https://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
eng_freq = dict(zip(list('etaoinsrhdlucmfywgpbvkxqjz'),[12.02,9.1,8.12,7.68,7.31,6.95,6.28,6.02,5.92,4.32,3.98,2.88,2.71,2.61,2.3,2.11,2.09,2.03,1.82,1.49,1.11,.69,.17,.11,.1,.07]))

def calc_stdev(freq):
	vals  = [val in freq.values()]
	stdev = statistics.pstdev(vals)

print(eng_freq)
sys.exit(0)
tokens = {}

def add_token(l,i):
	sec = l[start:start + i]
	if tokens.get(sec,None):
		tokens[sec] += 1
	else:
		tokens[sec] = 1


with open ("Jurassic_Park_eng.txt",'r') as book:
	for line in book:
		line_list = line.lower().split()  
		for l in line_list:
			if not l.isalpha():
				l = ''.join([c for c in l if c.isalpha()])
			length = len(l)
			if length > 3:
				remaining = length
				start = 0
				while (remaining >= 3):
					i = random.choice([2,3])
					add_token(l,i)
					start += i
					remaining -= i
			elif length > 0:
				add_token(l,remaining)


tokens.pop('')
for letter in 'bcdefghjklmnopqrstuvwxyz':
	try:
		tokens.pop(letter)
	except KeyError:
		continue

print(len(tokens))
print(sorted(tokens.items(), key=lambda x: x[1], reverse=True))



