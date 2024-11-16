import re
import sys

eng_freq = list('eariotnslcudpmhgbfywkvxxzjq')
eng_freq = list('etaoinsrhdlucmfywgpbvkxqjz')


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


print(sorted(count_dict.items(), key=lambda x: x[1], reverse=True))
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

print(substituted)
