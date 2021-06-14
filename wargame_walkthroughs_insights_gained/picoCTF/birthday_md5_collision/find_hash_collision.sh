source ~/.bashrc

f1=$(md5sum file1.pdf | cut -f1 -d' ')
f2=$(md5sum file2.pdf | cut -f1 -d' ')
while [ $f1 != $f2 ]
do
	#/usr/bin/python3 make_pdf.py file1.txt file1.pdf & chmod a+r file1.pdf
	/usr/bin/python3 make_pdf.py file2.txt file2.pdf & chmod a+r file2.pdf
	f1=$(md5sum file1.pdf | cut -f1 -d' ')
	f2=$(md5sum file2.pdf | cut -f1 -d' ')
	echo "$f1 $f2"
	sleep 0.9
	if [ "$f1" == "$f2" ]
		then echo "they're equal"
	fi
done
