ELF_bytes = ""
with open("bytes.txt","r") as f:
	for line in f:
		ELF_bytes += line


#print(ELF_bytes)

def not_so_fast(ELF_bytes,key):
	message = ""
	try:
		for i in range(len(ELF_bytes)):
			message += chr(ord(ELF_bytes[i]) - int(key))
		return message
	except Exception as e:
		return f"\nInvalid key: {key}\n"

j=0
for i in range(-292530,292530):
	msg = not_so_fast(ELF_bytes,i)
	if "elf" in msg.lower():
		with open(f"newBytes_{j}.{i}.txt","a") as file:
			file.write(msg)
		print(f"found one! key = {i}")
		j += 1;

"""keys = list(range(-1000,-500))
for i,key in enumerate(keys):
	with open(f"newBytes_{i}.txt","a") as file:
		file.write(not_so_fast(ELF_bytes,key))
"""

"""for key in keys:
	try:
		not_so_fast(ELF_bytes,key)
	except Exception as e:
		continue

with open("newBytes.txt","a") as file:
	file.write(not_so_fast(ELF_bytes,key))
"""
