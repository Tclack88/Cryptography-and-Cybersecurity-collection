eng_freq = list('eariotnslcudpmhgbfywkvxxzjq')
eng_freq = list('etaoinsrhdlucmfywgpbvkxqjz')
eng_freq = list('eationsrhdlucmfywgpbkqvxjz')
eng_freq = list('eitaonsrhdlumcfywgpbkvxqjz')
eng_freq = list('wxirmahtlycbpqsdnegfkujvoz')


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

substituted = translate(count_dict,eng_freq)
print(substituted)


def translate2(content):
	mapper=dict(zip('oveycmqlgzphftruxnsaiwdkbj','abcdefghijklmnopqrstuvwxyz'))
	print(mapper)
	substituted = ''
	for c in content:
		if mapper.get(c,None):
			substituted +=  mapper.get(c)
		else:
			substituted += c
	return substituted	

print(translate2(content))
