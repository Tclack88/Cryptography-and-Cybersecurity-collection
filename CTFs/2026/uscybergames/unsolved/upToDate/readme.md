INCOMPLETE

#progress

We can see from the code that chunks of the original message are being divided into 5 buckets, then headers are being appended to the packets as well as "bad packets". My strategy was to first find out how long the original message was (something called zencode)

I did this by passing in severals 1's in the input and incrementing until the length of the output matched that of the provided message. 271 was this length, the full message after all the headers and "bad packets" was 1452.

I then thought I could find the original message by passing in 271 1's, 271 2's, 271 3's and seeing what was similar with the output. The thought process was information was being added to the original messages, so if I subtract out the differences, I can get the original message. Unfortunately, I saw what I wanted. I was getting my original message back, and I assumed it was working as intended.

```python
r1=chall('1'*271)
r2=chall('2'*271)
r3=chall('3'*271)
r4=chall('4'*271)
r1 = np.array([i for i in r1])
r2 = np.array([i for i in r2])
r3 = np.array([i for i in r3])
r4 = np.array([i for i in r4])


mask1 = np.not_equal(r1,r2)
mask2 = np.not_equal(r2,r3)
mask3 = np.not_equal(r3,r4)
print(r3[mask1 & mask2 & mask3 & mask4])  # returns 271 3'
```

I then wanted to find the order. Knowing it was 271 characters and evenly distributed, 271/5 = 54 with a remainder. So I tried the same as above but passing in 12345 and seeing the output to figure out the re-order, because these would be

```
rn = chall('abcde'*54+'0') # <-- Trailing zero just to stand out
rn = np.array([i for i in rn])

mixed_numbers = rn[mask1 & mask2 & mask3 & mask4]
print(mixed_numbers)
```

With this I was able to see the order was: 2,5,1,4,3 (54 2's, 54 5's 54 1's +0, .. etc). I had all the pieces I thought, so I passed in the original message, applied the same mask and reordering to get an output:

```
r6 = """ the output, very long """
mixed = r6[mask1 & mask2 & mask3]
print(mixed)

two = mixed[:54]
five = mixed[54:108]
one = mixed[108:163]
four = mixed[163:217]
three = mixed[217:]
out = np.empty((one.size+two.size+three.size+four.size+five.size), dtype=one.dtype)
```
 The output: `6e0d19e890de06f940ba0000c5403f450d0b0811c00814c00802c00800c00805c00810c00839c00838c00871c00823c00814c00821c00814c00834c00873c00820c00871c00814c00826c00823c00875c00823c00814c00825c00830c00876c00826c00836dba0000c540b590d00842ba00006f20209e03f450b0029e483812820e0b5999b0dada` 

I can see some patterns, like "0811c00814c00802c00800c...." These might be the other things appended, but I know I'm not getting the original message back, because when I went back and tested letters instead of numbers (abcde instead of 12345) I was also getting numbers back. The output was being reduced to the last digit of its hexadecimal value or something, so I called it here.

