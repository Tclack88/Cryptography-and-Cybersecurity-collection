# find GCD
# uggcf://pelcgbunpx.bet/pbhefrf/zbqhyne/tpq/

def gcd(a,b):
	# Euclid's algorithm
	larger,smaller = max(a,b), min(a,b)
	if larger%smaller == 0:
		return smaller
	larger, smaller = smaller, larger%smaller
	return gcd(larger,smaller)

#print(gcd(12,8))
print(gcd(66528,52920))

# Extended Euclidean algorithm
# uggcf://pelcgbunpx.bet/pbhefrf/zbqhyne/rtpq/
"""
Figured this out by pattern matching using 81 and 57 as an example
Q	A	B	R
1	81	57	24
2	57	24	9
2	24	9	6
1	9	6	3
2	6	3	0

From here, we throw away the last row (it's merely to find terminating condition). Then we reverse substitute back up keeping in mind: a = q*b + r, we rearrange to find r = q*b - a
3	=	1(9)	-	1(6)			# first term
	=	1(9)	-	(24 - 2(9))		# express 6 from 24 and 9 
	=	3(9)	-	1(24)
	
3	=	3(9)			-	1(24)	# express 9 from 57 and 24
	=	3(57 - 2(24)) 	-	1(24)	
	=	3(57)			-	7(24)

3	=	3(57)	-	7(24)			# express 24 from 81 and 57
	=	3(57)	-	7(81 - 57)
	=	10(57)	-	7(81)

Writing this out in order found of factors in front of the larger term (a) , the smaller term (b), and the quotient (q) carried forward:
a	b	q
 1	-1	1
-1	 3	2
 3	-7	2
-7	10	1

Here, it's clear that b carries forward to the next a. And based on the math above, each b can be found as:

	b[i] = a[i-1] - q[i]*b[i-1]

(the first b[0] will be -q[0])
"""

def GCD(a,b, Q=[],A=[],B=[],R=[]):
	# Euclid's algorithm carrying forward information
	larger,smaller = max(a,b), min(a,b) # redundant. For 1st step
	Q.append(larger//smaller)
	A.append(larger)
	B.append(smaller)
	R.append(larger % smaller)
	if R[-1] == 0:
		return Q,A,B,R
	return GCD(B[-1],R[-1],Q,A,B,R)

#GCD(81,57)

def extended_euclid(a,b):
	"""
	Perform GCD to get every stage of the new numbers a and b
	as well as their quotient and remainders
	"""
	Q,A,B,R = GCD(a,b)
	q = Q[-2::-1] # reversed Q ignoring last element
	a = [1]
	b = [-q[0]] # begin as negative value of this first q
	for i in range(len(q)-1):
		a.append(b[i])
		b.append(a[i] - q[i+1]*b[i])
	return a[-1],b[-1]

#print("81 and 57:\n\n")
#extended_euclid(81,57)
print(extended_euclid(26513,32321))


# Modular Arithmetic
#uggcf://pelcgbunpx.bet/pbhefrf/zbqhyne/zqvi/
"""
No solution needed here, just notes. This mathologer video:
https://www.youtube.com/watch?v=_9fbBSxhkuA
Has a great informal, visual proof using rings showing fermat's little theorem.
Making a ring of 7 beads with 4 colors (and rotation under symmetry makes one ring the same as another)
For 4 choices of each 7 slots, we have:
4*4*4*4*4*4*4 of 4^7 total choices. But we don't want the monocolors, so subtract 4 away getting 4^7 - 4. Finally, to take into account the symmetry, we divide by 7 to remove those "extras"
(4^7-4)/7   This doesn't hold for non-primes, but we can say generally:
(a^p - a)/p = some integer value (n)
or a^p - a = p*n = p = 0 (mod p)
(under modular arithmeticp goes into a multiple of p some number of times with 0 as remainder
a^p = a  (mod p)
can divide both siees by a
a^(p-1) = 1  (mod p)
Can do it again
a^(p-2) = a^(-1)  (mod p)
This last one can be used to find the modular inverse. I.e. what you  multiply a by (under mod p) to get 1
"""

#uggcf://pelcgbunpx.bet/pbhefrf/zbqhyne/ebbg0/
"""
non-quadratic residue
This is just the value after squaring and moding
for al vals in 5:
(0**2)%5 = 0 (often 0 is ignored)
(1**2)%5 = 1
(2**2)%5 = 4
(3**2)%5 = 4
(4**2)%5 = 1

here, 1 and 4 are the quadratic residues
the rest (2,3) are quadratic non-residues

For an odd prime number, the number of quadratic residues is given by:
	(N-1)/2   (including 0 in the count, it's (N+2)/2 )
"""
# Va gur orybj yvfg gurer ner gjb aba-dhnqengvp erfvqhrf naq bar dhnqengvp erfvqhr. Svaq gur dhnqengvp erfvqhr naq gura pnyphyngr vgf fdhner ebbg. Bs gur gjb cbffvoyr ebbgf, fhozvg gur fznyyre bar nf gur synt.

p = 29
ints = [14,6,11]

def find_smallest_residue(p, ints):
	for i in range(1,p):
		qr = (i**2)%p
		if qr in ints:
			print(i)
			break

find_smallest_residue(p,ints)

# uggcf://pelcgbunpx.bet/pbhefrf/zbqhyne/ebbg1/
# Legendre Symbol

