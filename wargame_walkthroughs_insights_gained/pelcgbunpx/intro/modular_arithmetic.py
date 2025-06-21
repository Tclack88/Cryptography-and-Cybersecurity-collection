# uggcf://pelcgbunpx.bet/pbhefrf/zbqhyne/tpq/

def gcd(a,b):
	# Euclid's algorithm
	larger,smaller = max(a,b), min(a,b)
	if larger%smaller == 0:
		return smaller
	larger, smaller = smaller, larger%smaller
	return gcd(larger,smaller)

print(gcd(12,8))
print(gcd(66528,52920))

