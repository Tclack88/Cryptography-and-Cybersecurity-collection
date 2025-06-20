# Block Breaker
This was an AES-ECB (electronic code block) challenge (my first). It gets broken by consecutively guessing the last byte (explained in details below)  

## contents:

	* tests
		* challenge.py simulates the challenge AES-ECB oracle
		* ECB_decode_general.py the developed exploit
		* various flags of different lengths for testing
	* break_challenge.py the final exploit built from the core of ECB_breaker.py

## Theory

A listener is taking in strings that resemble hex (00-ff). Then pre-pending that to the flag text. This block is then padded (if needed) to 16 byte blocks and then run through the AUS-ECB encryption. The resulting ciphertext is returned.

Examples of some input and the resulting responses

```
> aa   (1 byte)
99fb80a0e630dfa7d6f83478a67516bc
abe37d3dec0b3ef36447ac18c2533943
> aaaa (2 bytes)
e908b642aa819a52a8c1a9b3ed78eb69
ada710be3435fb81d068e67399fd12f1
.
.
.
> aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa	(16 bytes)
fc934f43b30f9ed0e8c04d9cad87a2f4
f9750ee7ae07d79cfdd0f11ff316f4c3
ea56773fbdde1b2a8b30261707147e3d
```

Just to demo, I'll add another 16 bytes of a's
```
> aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (32 bytes)
fc934f43b30f9ed0e8c04d9cad87a2f4	(16 bytes a)
fc934f43b30f9ed0e8c04d9cad87a2f4	(16 bytes a)  <-- notice the repeat
f9750ee7ae07d79cfdd0f11ff316f4c3	(16 bytes flag)
ea56773fbdde1b2a8b30261707147e3d	(16 bytes of hex 16, (101010 ...10)
```

Adding one more byte of a's:
```
> aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (33 bytes)
fc934f43b30f9ed0e8c04d9cad87a2f4
fc934f43b30f9ed0e8c04d9cad87a2f4
99fb80a0e630dfa7d6f83478a67516bc  "a + {most of flag except last char"
abe37d3dec0b3ef36447ac18c2533943  "}..............."
```

We know the last line is a "}" (hex 7d) followed by 15 15's (hex 0f).
So this last block should be encoded if I pass in the following:

```
> 7d0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f ( "}" + 15 hex15 bytes)
abe37d3dec0b3ef36447ac18c2533943  <--- same as last block above!
f9750ee7ae07d79cfdd0f11ff316f4c3
ea56773fbdde1b2a8b30261707147e3d
```

It can be more obvious with the first and last block being the same if I add 15 more bytes of a's (could be anything though), because after being prepended, the input of each block should look like:

```
INPUT:
7d0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f{flag-flag-flag-flag......flag
\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f <-- (I wrote "\}" but it's really 7d)

OUTPUT:
abe37d3dec0b3ef36447ac18c2533943  <--these are the same!
99fb80a0e630dfa7d6f83478a67516bc
abe37d3dec0b3ef36447ac18c2533943  <--these are the same!
```

Now I actually know the next is a `g`, but if I didn't, I could start guessing
INPUTS 
```
a} ......  (--as hex and padding--> ) 617d0e0e0e0e0e0e0e0e0e0e0e0e0e0eaaaa
b} ......  (--as hex and padding--> ) 627d0e0e0e0e0e0e0e0e0e0e0e0e0e0eaaaa
c} ......  (--as hex and padding--> ) 637d0e0e0e0e0e0e0e0e0e0e0e0e0e0eaaaa
.
.
.
g} ......  (--as hex and padding--> ) 677d0e0e0e0e0e0e0e0e0e0e0e0e0e0eaaaa

OUTPUTS
a} ......
> 617d0e0e0e0e0e0e0e0e0e0e0e0e0e0eaaaa
6f376f28ba75a7fd1c73a73e136cd4d5
e908b642aa819a52a8c1a9b3ed78eb69
ada710be3435fb81d068e67399fd12f1

b} ......  
> 627d0e0e0e0e0e0e0e0e0e0e0e0e0e0eaaaa
75c231b344f063546740550ca8fbce26
e908b642aa819a52a8c1a9b3ed78eb69
ada710be3435fb81d068e67399fd12f1

c} ......  
> 637d0e0e0e0e0e0e0e0e0e0e0e0e0e0eaaaa
5e676571f78bd5426c85f05f21edf0ca
e908b642aa819a52a8c1a9b3ed78eb69
ada710be3435fb81d068e67399fd12f1
.
.
.

g} ......  
> 677d0e0e0e0e0e0e0e0e0e0e0e0e0e0eaaaa
ada710be3435fb81d068e67399fd12f1 <---- match
e908b642aa819a52a8c1a9b3ed78eb69
ada710be3435fb81d068e67399fd12f1 <---- match
```

So the algorithm is clear. Guess ascii chars, adding the appropriate padding + junk until the next final byte is found. Carry that found byte value forward, and decrement the padding. Until the padding reaches 00

Let's discuss the padding. Assuming a block size of 16 through the whole challenge. If the flag is 4 bytes and my guess is 2, that's 6 bytes together. This submission alone would then be padded with 10 more bytes of hex 10 (`0a`). But this wouldn't produce symmetric blocks. When guessing the first block, I would need that to overlow one then we know the algorithm would add 15 hex 15 (`0f`) blocks. I can just make my padding equal to that block. If the flag was 16 bytes and I could somehow not give any input, the flag would be processed, but who's to say the last block wasn't hex `01`? To avoid any ambiguity, a block of 16 hex 16 (`10`) would be added. 

In smaller cases, it would just be of coruses rounded up to the difference, so we need a way to find the difference between the flag size and the next block rounded up. After some observation, it's clear that we would always have the guess length then add padding of size (next_block_up - flag_size) plus an additional block size always.

In total for this example flag length 16 (it's block rounded up then to 32), this is how many chars I need to add to make a well aligned block: It's always going to be  the length of the guess + the length of the flag rounded up to the nearest multiple of 16.
```
CRYPT{fake_flag}   (16)			1		+ 16	+16           
							(len guess)	 (32-16)  (always)
							padding_val : 16-1  = 12  padding_len(16+16)
\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f\C\R\Y\P\T\{\f\a\k\e\_\f\l\a\g
\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
```


For different lengths:
longer than 16:

```
24 length flag (eg)
"{this_is_a_longish_flag}" to hex 
\{ffffffffffffffffffffffffffffffffffffffffffff\}

\{ffffffffffffffffffffffffffffff
ffffffffffffff\}0808080808080808

aaaaaaaaaaaaaaaa\{ffffffffffffff   8 bytes will push a new line (24+8=32)
ffffffffffffffffffffffffffffff\}
10101010101010101010101010101010

aaaaaaaaaaaaaaaaaa\{ffffffffffff   9 bytes will push last val to new line
ffffffffffffffffffffffffffffffff
\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f


\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f   25  (  '{'  +  24 0f's (15)  )
0f0f0f0f0f0f0f0f0f\{ffffffffffff   1	+	  8		+		16
ffffffffffffffffffffffffffffffff len(guess)   (32-24)      always
\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f	padding_val: 16-1


\g\}0e0e0e0e0e0e0e0e0e0e0e0e0e0e   26  (  'g}'  +  24 0e's (14)  )
0e0e0e0e0e0e0e0e0e0e\{ffffffffff
ffffffffffffffffffffffffffffffff
\g\}0e0e0e0e0e0e0e0e0e0e0e0e0e0e

\a\g\}0d0d0d0d0d0d0d0d0d0d0d0d0d  27   ('ag}'  +  24 0d's (13)
0d0d0d0d0d0d0d0d0d0d0d\{ffffffff
ffffffffffffffffffffffffffffffff
\a\g\}0d0d0d0d0d0d0d0d0d0d0d0d0d


\_\a\_\l\o\n\g\i\s\h\_\f\l\a\g\}  40  ('_a_longish_flag}' + 24  10 (16)
10101010101010101010101010101010
1010101010101010\{\t\h\i\s\_\i\s
\_\a\_\l\o\n\g\i\s\h\_\f\l\a\g\}


\s\_\a\_\l\o\n\g\i\s\h\_\f\l\a\g  41  ('s_a_longish_flag}' + 24 0f (15)
\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f\{\t\h\i\s\_\i  comparing first 2 and last 2 lines !
\s\_\a\_\l\o\n\g\i\s\h\_\f\l\a\g  16*ceil(guesslength/16)   ????
\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f  

s_is_a_longish_flag} guess = 20      16*ceil(20/16) = 32 => compare 2

\s\_\i\s\_\a\_\l\o\n\g\i\s\h\_\f	 20  + 12  (0c)  = 32
\l\a\g\}0c0c0c0c0c0c0c0c0c0c0c0c
0c0c0c0c0c0c0c0c0c0c0c0c\{\t\h\i
\s\_\i\s\_\a\_\l\o\n\g\i\s\h\_\f
\l\a\g\}0c0c0c0c0c0c0c0c0c0c0c0c
```

Short flag examples:

```
{short_flag}  (12)
\{\s\h\o\r\t\_\f\l\a\g\}        start: 4 to get to end, + 1 to overflow +
									   16 (  { + 15 0f's)  = 21
										
\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f 	12 -> 32   (add 20)  + 1 to push over
0f0f0f0f0f\{\s\h\o\r\t\_\f\l\a\g	so that's ( { + 20 0f's)
\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f


\f\l\a\g\}        (5)			  5        +    4     + 16       = 25
								len(guess)   (16-12)  (always)
									16 - 5 = 11 (padding = 0b)
\f\l\a\g\}0b0b0b0b0b0b0b0b0b0b0b
0b0b0b0b0b0b0b0b0b\{\s\h\o\r\t\_
\f\l\a\g\}0b0b0b0b0b0b0b0b0b0b0b


\r\t\_\f\l\a\g\}  (8)			(+8 to equal 16) => trailing 08s
								8          +   4     +   16
								len(guess)   (16-12)   + always
								padding: 16 - 8 = 8

\r\t\_\f\l\a\g\}0808080808080808
080808080808080808080808\{\s\h\o
\r\t\_\f\l\a\g\}0808080808080808
```

Extra long flag examples:

```
{this_is_quite_a_long_flag_maybe_more_than_32}   (46)
												46 -> 48   +2
first guess (get }):			1		+	2	+	16		 = 19
								(len guess) (48-46) (always)
									padding = 16-1 = 15  (0f)

\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f\{\t\h\i\s\_\i\s\_\q\u\i\t
\e\_\a\_\l\o\n\g\_\f\l\a\g\_\m\a
\y\b\e\_\m\o\r\e\_\t\h\a\n\_\3\2
\}0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f


ong_flag_maybe_more_than_32}  (28)		28   	+	2	+	16	= 46  
									len(guess) (48-46)  (always)
										padding:  32-28 = 4  (04)


\o\n\g\_\f\l\a\g\_\m\a\y\b\e\_\m
\o\r\e\_\t\h\a\n\_\3\2\}04040404
0404040404040404040404040404\{\t
\h\i\s\_\i\s\_\q\u\i\t\e\_\a\_\l
\o\n\g\_\f\l\a\g\_\m\a\y\b\e\_\m
\o\r\e\_\t\h\a\n\_\3\2\}04040404



shooFISHOOOO!!!! 			 (16)	16  	+    8    + 16   = 40
								  len(guess)  (32-24)   (always)
									padding_val: 32-16 = 16 (10)
\s\h\o\o\F\I\S\H\O\O\O\O\!\!\!\!  
10101010101010101010101010101010
1010101010101010\F\i\s\h\o\o\f\i
\s\h\o\o\F\I\S\H\O\O\O\O\!\!\!\!
10101010101010101010101010101010
```

This should be sufficient to see all the patterns. The algorithm is built to cover this. The biggest trouble I had was sending and receiving through the listener on netcat. Because I have to send bytes. But my string I'm sending is hex. So it has to be unhexed on the other end. It's basically double hexed. My string hexed (eg. aaaaaa goes to `\xaa\xaa\xaa`. But this then gets byte encoded again. Then the response has to be decoded (unhexed) then that has to be unhexed again to return the string that just appears like hex. Quite confusing.
