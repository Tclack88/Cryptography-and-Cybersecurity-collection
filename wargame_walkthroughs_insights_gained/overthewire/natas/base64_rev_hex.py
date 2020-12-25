# Python script for level 8 natas
import base64
encoded = '3d3d516343746d4d6d6c315669563362'

step1 = bytes.fromhex(encoded)

print(step1)
step2 = step1[::-1]
print(step2)
step3 = base64.b64decode(step2)#.decode(step2)
print(step3)

print('oneliner:')
print(base64.b64decode((bytes.fromhex(encoded))[::-1]))

