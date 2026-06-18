import re

infile = 'wire.txt'

content = ""
with open(infile) as f:
	for line in f:
		content += line

spaces = re.compile('\s+')
space_list = spaces.findall(content)
num_list = [len(s) for s in space_list]
#print(num_list)

mapping = {2:'.',4:'-',3:' '}

print(''.join([mapping[i] for i in num_list[:-1]]))
