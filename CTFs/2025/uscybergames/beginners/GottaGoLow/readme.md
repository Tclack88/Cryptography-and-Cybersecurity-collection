# Gotta Go Low
This is a weak RSA encryption. I don't fully understand it yet.

## content
* challenge.py -- details how the files were created. It's not used directly in the solution, just for understanding the process
* output.txt -- provided, the resulting large prime `n` the base exponent 3 and the `ciphertext`, an encrypted result from this large integer multiplication. 

## solution

The name "Gotta Go Low" is referencing that base 3. It's too low to be cryptologically sound. Usually 65537 is used. I belive the process goes like this:

A large number (created from the product of two primes) are multiplied. The base (3 in this case) is raised to the power of the number we want to encrypt (maybe a hexadecimal representation of the flag) and then it's moded with that large number n. The fact that that base is so low means we haven't gotten a large enough number for the modulus to do anything, so the resulting value is really just the flag's number cubed.

It's like if we were doing 3^2 mod 11. 3^2 is 8, and mod 11 is 8, so we can't hide what that number is.

Finding the cubed root directly with python using `ciphertext**(1/3)` doesn't get us anywhere, it's just an approximation. So we can find it using a binary search like algorithm. Setting the left value to 0 and the right value to the large value. We can then find the middle value and cube it. If it's equal to the flag, we found it. Otherwise if it's larer or smaller, we adjust our right and left values and continue this process until it's found. Details are in the`decrypt.py` script provided. The output below:


`b'SVBGR{l0w_3xp0n3nt5_@r3_n0t_s@fe}'`
