
hex_in = "4500001c000100004001a88bc0a8019d080808080800f7ff00000000"
shift = 83-69

bytes_in = bytes.fromhex(hex_in)


for i in range(200):
	msg = ""
	for b in bytes_in:
		try:
			shifted = chr(b-i)
			msg += shifted
		except Exception as e:
			continue
	print(msg)

