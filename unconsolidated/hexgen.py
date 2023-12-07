#!/usr/bin/env python3

# The purpose of this program is to generate 16 byte keys such that when
# AES encrypted with the given X, the corresponding ciphertext's last hex byte
# will be '00'. This is achieved by generating hex numbers, padding the front
# with 0's (until 16 bytes exist) then AES encrypting and checking the results

from Crypto.Cipher import AES
import binascii

X = b'\x10\x04\x20\x18' + 12 * b'\x00'


def AES_Encrypt(key,plaintext):
    encryption = AES.new(key, AES.MODE_ECB)
    ciphertext = encryption.encrypt(plaintext)
    return ciphertext


i = 0
n = 16
while n >= 0:
    s = str(hex(i))[2:]
        # the hex number with '0x' removed, s is the pre-padded, non-zero
        # part of the key (to be expanded shortly to proper length)
    n = 16 - len(s)
    if n % 2 == 0:
        n += 1
        # n is the number of pairs hex bytes, n will decriment until 
        # reaching 0 in order to continue to generate the desired keys

    s = s.zfill(32)
    key = bytes.fromhex(s)
    ciphertext = AES_Encrypt(key,X)
    if ciphertext[-1] ==0:
        print("\n\n\n\n\n\nkey:",'---',key)
        print("Key as hex string:",key.hex())
        print("\nciphertext:","---",ciphertext)
        print("ciphertext as hex string:",ciphertext.hex())
        # make 32 char long (which corresponds to 16 bytes in hex) to get key
        # generate ciphertext, print if ciphertext matches desired criteria
    i += 1
