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

def is_uppercase_letters(bytes_seq):
    # Check if all bytes correspond to ASCII uppercase letters
    return all(65 <= b <= 90 for b in bytes_seq)

ciphertext_hex = c1
keys_list = ["PLAN", "NEVER", "SECRET", "OUR", "HIGHER", "CLASSIFIED", "WILL", "BE", "LEET"]

cipher_bytes = list(bytes.fromhex(ciphertext_hex))

for key in keys_list:
    key_bytes = key.encode()  # encode plaintext key to bytes
    key_len = len(key_bytes)
    max_start = len(cipher_bytes) - key_len + 1

    for start in range(max_start):
        slice_bytes = cipher_bytes[start:start+key_len]
        # XOR each byte
        xored = bytes([b ^ k for b, k in zip(slice_bytes, key_bytes)])
        # Check if all are uppercase letters
        if is_uppercase_letters(xored):
            # Create a display with the decoded uppercase string in place
            output = ['-' for _ in range(len(cipher_bytes))]
            for i, ch in enumerate(xored):
                output[start + i] = chr(ch)
            print(''.join(output))
