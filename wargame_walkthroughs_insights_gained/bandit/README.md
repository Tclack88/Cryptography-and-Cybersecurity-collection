# Lessons learned for bandit wargame:
[Bandit wargame on overthewire.org](https://overthewire.org/wargames/bandit/)

files beginning with a "-":

can't `rm` or `vim` or `cat` it normally, must use something like:

```bash
cat ./-file
```







for loops in bash: 

(list the file types)
```bash
for i in $(ls); do echo $i ; done
```

(for actual challenge, had to find which dashed file contained an ASCII text:

```bash
for i in $(ls); do file ./$i; done
```







## 5-6
find files that are a certain size (recursive by default)

```bash
find . -size 1033c      <--- (the c is bytes, so 1033 bytes)
```






## 6-7
find files with a specific ownership (group and/or user)

```bash
find / -user USER -group GROUP
```







## 8-9
uniq -- so apparently uniq doesn't return unique lines, it returns duplicated
-u tells you what is `uniq` (not duplicated) and `-d` tells what is duplicated
so for the following:
```
a
b
c
a
b
c
c
d
```

`uniq -u` gives:

```
a
b
c
a
b
c
d
```
`uniq -d` gives

```
c
```

since I want to find the only ACTUALLY UNIQUE line, I'd have to sort, then use
uniq -u. so the following command returns "d":

`sort file.txt | uniq -u `









## 9-10
find strings within a file:
```bash
strings file.txt (which can of course be grep'd to find certain matches
```







## 10-11
base 64

to encode something to base 64:  
```bash
echo "Mikayla Smells" | base64
```

to decode:
```bash
echo "TWlrYXlsYSBTbWVsbHMK" | base64 -d
```






## 11 - 12

tr -- translate

here's my rotate by 13 script, shifting all lower and upper cases by 13 letters

```bash
cat data.txt | tr [a-m,n-z,A-M,N-Z] [n-z,a-m,N-Z,A-M]
```
only improvement is I can remove the commas and eliminate brackets
```bash
cat data.txt | tr a-mn-zA-MN-Z n-za-mN-ZA-M
```

!!!!! or in VIM, just highlight in visual mode and use `g?` !!!!!




## 12-13
unzipping many files

```bash
gzip     gzip -d blah.gz

bzip2    bzip2 -d blah.bz2

# and tar of course  
tar -xfv blah.tar.gz
```




## 13,14,15,16,17   

lots of socket/port stuff I need to learn




## 19-20 find out which files are owned by root and have an setuid binary:
with that setuid binary you can maybe get root access if you're clever

```bash
find / -user root -perm -4000 -print 2>/dev/null
```





## 20-21 cool port trick:
setup a listening port:

`nc -lvp 3000`   (listen verbosely on port 3000)

then in another terminal (or use tmux and `ctrl-b %` to split panes,
`crtl-b o` to move between panes)
use 
`nc -v localhost 3000` to connect
Anything typed in one will show in the other







## 24-25
BRUTE FORCE

This was my poor attempt (it worked, but not every connection would be made
it was also slow)

(Background: a Daemon is listening on port 30002 if it receives the password
for bandit24 plus a 4-digit secret pin, it returns the password for bandit25)

```bash
#!/bin/bash

for i in {0000..9999}
do
echo UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ $i | nc localhost 30002 >> output.txt &
done

echo ALL DONE! 

echo "sorting ... here are the repeated results:"
sort output.txt | uniq -d

echo "here are the unique results:"
sort output.txt |uniq -u
```

Here's a way that works better (create a dictionary of pins and pipe them to nc

```bash
#!/bin/bash

for i in {0000..9999}
do echo UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ $i >> pins
done && cat pins | nc localhost 30002
```

(NOTE: the `&&` makes the next command execute if the previous one was successful, indicated by error code of 0. Contrast to `||` which executes if previous command failed. It has to be placed where it is, not on a newline)








## 26-27
while waiting for "more" command to load pages, pressing "v" will take you to vim
within vim, you can actually edit any other document. 

`:e /path/name/here/document.txt` will let you do that
