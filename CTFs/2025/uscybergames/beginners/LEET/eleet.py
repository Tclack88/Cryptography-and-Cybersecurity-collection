import sys
"""
To see if you are truly LEET enough to make it in, we're giving you some encrypted communications that we've captured from some federal agencies. We know that they used XOR encryption with the same key for both, and that the message text contain all uppercase english letters.

1. 5c623c61545f63270c4047724e114d52794e16485f7b4e034433652b1744527b2b0520
2. 40612c0653687b270649477e20065e4667311549566823044f4c7e201e435f762d0a7c
We've also heard a few code words from them. I don't know if they will be of much help, but they were PLAN, NEVER, SECRET, OUR, HIGHER, CLASSIFIED, WILL, and BE. Maybe they were used in one of the messages?

Can you crack it?
"""

c1 = "5c623c61545f63270c4047724e114d52794e16485f7b4e034433652b1744527b2b0520"

c2 = "40612c0653687b270649477e20065e4667311549566823044f4c7e201e435f762d0a7c"


keys = ["PLAN", "NEVER", "SECRET", "OUR", "HIGHER", "CLASSIFIED", "WILL", "BE", "LEET"]
CAPS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
c1 = bytes.fromhex(c1)
c2 = bytes.fromhex(c2)

#blank = bytes.fromhex('00')*6
#print(blank)
#listed = list(blank)
#listed[3] = 0xaa
#print(listed)
#print(bytes(listed))
print(c1)

"""
ct = list(c1)
for key in keys:
	#print(list(bytes(key,'utf-8')))
	key_bl = list(bytes(key,'utf-8')) # bl== byte_list
	for i in range(len(c1)-len(key)+2):
		blank = list(bytes.fromhex('00')*len(c1))
		ct_slice = ct[i:i+len(key)-1] 
		xored = [ct_slice[i]^key_bl[i] for i in range(len(ct_slice))]
		xor_bytes = bytes(xored)
		xor_word = xor_bytes.decode('utf-8')
		if xor_word.isalpha() and xor_word.isupper():
			blank[i:i+len(key)-1] = key_bl
			blank = [chr(c) for c in blank]
			blank = ''.join(["-" if c == '\x00' else c for c in blank])
			print(blank)


ct = list(c2)
for key in keys:
	#print(list(bytes(key,'utf-8')))
	key_bl = list(bytes(key,'utf-8')) # bl== byte_list
	for i in range(len(c1)-len(key)+2):
		blank = list(bytes.fromhex('00')*len(c1))
		ct_slice = ct[i:i+len(key)-1] 
		xored = [ct_slice[i]^key_bl[i] for i in range(len(ct_slice))]
		xor_bytes = bytes(xored)
		xor_word = xor_bytes.decode('utf-8')
		if xor_word.isalpha() and xor_word.isupper():
			blank[i:i+len(key)-1] = key_bl
			blank = [chr(c) for c in blank]
			blank = ''.join(["-" if c == '\x00' else c for c in blank])
			print(blank)
"""

ct1 = list(c1)
ct2 = list(c2)
ct = [ct1[i]^ct2[i] for i in range(len(ct1))]
for key in keys:
	#print(list(bytes(key,'utf-8')))
	key_bl = list(bytes(key,'utf-8')) # bl== byte_list
	for i in range(len(c1)-len(key)+2):
		blank = list(bytes.fromhex('00')*len(c1))
		ct_slice = ct[i:i+len(key)-1] 
		xored = [ct_slice[i]^key_bl[i] for i in range(len(ct_slice))]
		xor_bytes = bytes(xored)
		xor_word = xor_bytes.decode('utf-8')
		if xor_word.isalpha() and xor_word.isupper():
			blank[i:i+len(key)-1] = key_bl
			blank = [chr(c) for c in blank]
			blank = ''.join(["-" if c == '\x00' else c for c in blank])
			print(blank)

"""

	p = bytes(key,'utf-8')
	decoded1 = bytes([c1[i]^p[i] for i in range(len(p))])
	decoded2 = bytes([c2[i]^p[i] for i in range(len(p))])
	decoded3 = bytes([c2[i]^p[i]^c1[i] for i in range(len(p))])

	decoded1 = decoded1.decode('utf-8')
	decoded2 = decoded2.decode('utf-8')
	decoded3 = decoded3.decode('utf-8')
	if "SVBRG" in decoded1 or "SVBGR" in decoded1:
		print("\t",decoded1)
	if "SVBRG" in decoded2 or "SVBGR" in decoded2:
		print("\t",decoded2)
	if "SVBRG" in decoded3 or "SVBGR" in decoded3:
		print("\t",decoded3)

for key in keys:
	#print(p,len(p),len(c1),len(c2))
	p = bytes((key*20)[:35],'utf-8')
	decoded1 = bytes([c1[i]^p[i] for i in range(len(p))])
	decoded2 = bytes([c2[i]^p[i] for i in range(len(p))])

	decoded1 = decoded1.decode('utf-8')
	decoded2 = decoded2.decode('utf-8')
	print(decoded1)
	print(decoded2)
	print()

sys.exit(0)



count = 0
for k in keys:
	print(k,len(k))
	count += len(k)
print(count)
	
"PLAN", "SECRET", "OUR", "HIGHER", "CLASSIFIED", "WILL", "BE"
"PLAN", "NEVER", "SECRET", "HIGHER", "CLASSIFIED", "WILL"
"""

