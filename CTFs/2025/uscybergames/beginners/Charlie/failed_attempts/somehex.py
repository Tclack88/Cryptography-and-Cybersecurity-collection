string_bytes  = "".join("""bfa7 6f4e 3a55 9d37 4dff 0084 6f4d edfe
7f31 fe7f 1ac4 b6b9 ff00 979e 3fe2 5fff
0041 6ebf e38e f9fe 5401 ffd9 504b 0304
1400 0000 0800 6d74 b85a 7640 2926 2a42
0000 ec13 0100 0800 1c00 666c 6167 2e74
7874 5554 0900 037e 1f32 6898 1f32 6875
780b 0001 04e8 0300 0004 e803 0000 ec5d
6bb3 b238 d6fd 41f9 102e 11c2 c720 202a
2237 01fd 0642 c01b 2a20 a0bf 7ee2 73ba
6ba6 dfb7 67ba 9faa 3e4e 4f15 a7ca da1e""".split())

bts = bytes(string_bytes,'utf-8')
shift = 100
for i in range(shift):
	shift = 50 - i
	msg = ""
	for b in bts:
		msg += chr(b+shift)
	print(msg)
