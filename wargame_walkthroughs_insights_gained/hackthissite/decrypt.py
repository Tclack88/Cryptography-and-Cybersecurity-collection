# Level 7 python decryption script
enc = "a65:;7=?"
enc = list(enc)
print(enc)
numeric = [chr(ord(e)-i) for i,e in enumerate(enc)]
print(''.join(numeric))
