import sys
from itertools import permutations
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

c1 = bytes.fromhex(c1)
c2 = bytes.fromhex(c2)

perms = permutations(keys)



guesses = ["OURSECRETPLANWILLBECLASSIFIEDHIGHER", "OURSECRETPLANWILLBEHIGHERCLASSIFIED"]

"""
for key in perms:
	key = '.'.join(key)
	p = bytes(key*(35//len(key)),'utf-8')
	decoded1 = bytes([c1[i]^p[i] for i in range(len(p))])
	decoded2 = bytes([c2[i]^p[i] for i in range(len(p))])
	decoded3 = bytes([c2[i]^p[i]^c1[i] for i in range(len(p))])
	print(f"c1: {decoded1}\nc2: {decoded2}\nc3: {decoded3}\n\n")
"""
for key in keys:
	key = (key*35)[:35]
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
"""
count = 0
for k in keys:
	print(k,len(k))
	count += len(k)
print(count)
	
"PLAN", "SECRET", "OUR", "HIGHER", "CLASSIFIED", "WILL", "BE"
"PLAN", "NEVER", "SECRET", "HIGHER", "CLASSIFIED", "WILL"
"""

res = """LOQ)W{YNZEAB>[RZN3BOY_,I[3ZEYKLC OFS5BcKEI[EX=RPF[+PDJA(SX:XYLS _OQ4T~^IOMC@/D@]X6FEJ_,TX6]BLC KJ\\+P~TL]@L@9^_XI6OM^Z!K\\6WG^NAA ^FR"ErZEHLBI,RQQ\\:ADKV/BI:YNKBOHDJ PFU3Kr]TFLEX"RV@R:FUEV(SG:^_EBHY""".split()
for re in guesses:
	#print(":::: ", res," ::::")
	re = '.'.join(re)
	for i in range(80):
		decode = "".join([chr(ord(r)+50-i) for r in re])
		#if "SVB" in decode:
		print(decode)
