import random
import string

def chall(zenc_code):
	random.seed(42)
	#zenc_code = """REDACTED"""
	#zenc_code = """0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"""
	#print(len(zenc_code)) 271

	# Split the Zen-C code into five chunks
	num_strides = 5
	chunks = [zenc_code[i::num_strides] for i in range(num_strides)]

	packets = []
	# Valid packets: [Magic: ZN (2 bytes)][Seq (1 byte)][Len (1 byte)][Payload (Len bytes)]
	for seq_id, text in enumerate(chunks):
		# Secure the payload by starting it with its sequence ID
		payload_str = str(seq_id) + text
		payload = payload_str.encode('utf-8')
		header = b'ZN' + bytes([seq_id, len(payload)])
		packets.append(header + payload)

	def random_payload(length):
		return "".join(random.choices(string.ascii_letters + string.digits, k=length)).encode('utf-8')

	# Noisy packet 1: Wrong magic bytes
	for _ in range(10):
		bad_magic = bytes(random.choices(range(256), k=2))
		if bad_magic == b'ZN':
			bad_magic = b'XX'
		rand_len = random.randint(5, 25)
		packets.append(bad_magic + bytes([random.randint(0, 255), rand_len]) + random_payload(rand_len))

	# Noisy packet 2: Wrong payload start (not matching with sequence ID)
	for _ in range(10):
		dup_seq = random.randint(0, num_strides - 1)
		rand_len = random.randint(5, 25)
		
		bad_payload = random_payload(rand_len)
		# Make sure the bad payload doesn't start with correct sequence ID
		if bad_payload.startswith(str(dup_seq).encode('utf-8')):
			bad_payload = b'X' + bad_payload[1:]
			
		packets.append(b'ZN' + bytes([dup_seq, len(bad_payload)]) + bad_payload)

	random.shuffle(packets)
	full_stream = b"".join(packets)
	hex_output = full_stream.hex()
	#print(hex_output)
	
	return(hex_output)
	#with open("output.txt", "w") as f:
	#	f.write(hex_output)

if __name__ == "__main__":
	
	r1=chall('1'*271)
	r2=chall('2'*271)
	r3=chall('3'*271)
	r4=chall('4'*271)
	r5=chall('r'*271)

	import numpy as np

	r1 = np.array([i for i in r1])
	r2 = np.array([i for i in r2])
	r3 = np.array([i for i in r3])
	r4 = np.array([i for i in r4])
	r5 = np.array([i for i in r5])
	r6 = np.array(list('5a4e0137316e6e3e6420746530202c62307830202c38377830202c64337830202c64327830202c64327830202c662074203420726e6572636265205a4e0215747a797368413650334d73486172414a4f43426e440ee02b0754593848684f363896510552766a37751947ba196b77505251654e4870437135516e75566459587965344a536e5a4e041446306a37656c4b506f6833704b4d7a4b47356d535a4e04373461206f0a6c6f2031317830202c30337830202c64327830202c30377830202c35327830202c3632780a6c65300a66206f20747220297d5a4e030d637569386b4252496736516a638ab9f21770447a664f767a31644f4f645458676c48696c433265595a4e010d686749714c536d4e71453430665a4e00383066692d692065645b2c34307830202c39337830202c31317830202c31317830202c33317830202c663320657978206f69647028286b3b0a5a4e000c776a5a524c394f6159735036db1907193835306b456e7964783971574341373949536a73384a4855642a87d81837355551537950783342706462494b6152646562754672455a4e0337336d29767b20633d317830202c35317830202c63317830202c33327830202c33377830202c303778303b206b203b2062637b6e615e290a5a4e0217494163773538637751507649323855356f6b586b7a6c35171887105954483878495a4d314a52636f72656f5a4e0111753137724e7938483668386c3771674154e2c0ae19674143373271466c3431734e4c6a5648574761756235325a745a4e010d795073745565433939656e71357fe2ea196969554855414b7739694555316a6a514b784b4470493651685a4e023732202820202020207830202c30307830202c31327830202c34377830202c36327830202c35337830205d20203d3220202020696820797d5a4e030c71576732316e594373586f62a3067d0d6e5450336641626e46626d4f485a4e02124c46784a7052613548535550776550757430'))
	rn = chall('abcde'*54+'y')
	rn = np.array([i for i in rn])
	mask1 = np.not_equal(r1,r2)
	mask2 = np.not_equal(r2,r3)
	mask3 = np.not_equal(r3,r4)
	mask4 = np.not_equal(r4,r5)
	print(len(r1))
	print(len(rn))
	print(r3[mask1 & mask2 & mask3 & mask4])
	#print(len(r3[mask1 & mask2 & mask4]))
	#print(r3[mask1 & mask2 & mask3])
	print(len(r3[mask1 & mask2 & mask4]))
	#print(len(r3[mask1 & mask2]))
	mixed_numbers = rn[mask1 & mask2 & mask3 & mask4]
	#mixed_numbers = rn[mask1 & mask2 & mask3]
	print(mixed_numbers)
	print(len(mixed_numbers))
	two = mixed_numbers[:54]
	five = mixed_numbers[54:108]
	one = mixed_numbers[108:163]
	four = mixed_numbers[163:217]
	three = mixed_numbers[217:]

	print(one)
	print(two)
	print(three)
	print(four)
	print(five)

	out = np.empty((one.size+two.size+three.size+four.size+five.size), dtype=one.dtype)
	out[0::5] = one
	out[1::5] = two
	out[2::5] = three
	out[3::5] = four
	out[4::5] = five
	print(''.join(out))
	print(''.join(out) == '12345'*54+'0')
	print(len(out))

	import sys; sys.exit(0)
	


	#mixed = r6[mask1 & mask2 & mask3 & mask4]
	mixed = r6[mask1 & mask2 & mask3]
	print(mixed)

	two = mixed[:54]
	five = mixed[54:108]
	one = mixed[108:163]
	four = mixed[163:217]
	three = mixed[217:]
	out = np.empty((one.size+two.size+three.size+four.size+five.size), dtype=one.dtype)
	out[0::5] = one
	out[1::5] = two
	out[2::5] = three
	out[3::5] = four
	out[4::5] = five
	print(''.join(out))
	print(len(out))
	#print(len(mixed))
	#reordered_nums = list(zip([one,two,three,four,five]))

