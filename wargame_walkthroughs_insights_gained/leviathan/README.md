# Leviathan Notes
[Leviathan wargame on overthewire.org](https://overthewire.org/wargames/leviathan/)

ltrace:

can run a file after calling this to see an output that may provide info:

ex in leviathan 1--->2
a file called `check` is here
```
-r-sr-x--- 1 leviathan2 leviathan1 7656 May 10 18:27 check
```

performing `ltrace ./check` returns:
```
bc_start_main(0x565556c0, 1, 0xffffd744, 0x565557a0 <unfinished ...>
printf("password: ")                             = 10
getchar(0xf7fc5000, 0xffffd744, 0x65766f6c, 0x646f6700password: PASSWORD

					(I typed in 'PASSWORD')

) = 80
getchar(0xf7fc5000, 0xffffd744, 0x65766f6c, 0x646f6700) = 65
getchar(0xf7fc5000, 0xffffd744, 0x65766f6c, 0x646f6700) = 83
strcmp("PAS", "sex")                             = -1
puts("Wrong password, Good Bye ..."Wrong password, Good Bye ...
)             = 29
+++ exited (status 0) +++
```
So it looks like a C++ or C or whatever code is running that does a string
comparison with "PAS" and "sex". This must mean that "sex" is the password
it is looking for



## 2 --> 3

in ltrace and strace, access(...) checks for permissions based on your
REAL user ID rather than your effective user ID

There exists a program (a binary file, can't be read)
```
-r-sr-x---  1 leviathan3 leviathan2 7640 May 10 18:27 printfile
Usage: ./printfile filename
```
Assumption (based on experimenting): this program reads a file if the 
permissions match (ltrace reveals this program does an "access" check and
it calls on /bin/cat)

Solution:

-make a file file with two spaces in the name
	ex: "mikayla smells.txt"
-make a soft symbolic link to the password containing file
	in this case "mikayla"
-Run the program on the two spaced text file

How it works (best guess):

`cat` will ignore the space and treat it as two separate files, so we want to 
"cat mikayla" but we can't do that directly since the symbolic link it follows
to doesn't match permission. But the file we create ("mikayla smells.txt") does
So the approved permissions allows the program to continue and "cat" will
be able to do its thing






## 5-->6
Another symbolic link example:

There is a file called "leviathan5"
```
-r-sr-x--- 1 leviathan6 leviathan5 7764 May 10 18:27 leviathan5
```
if ran (with ltrace) the following output is observed:
```
Cannot find /tmp/file.log
```

if we create a file ( `echo test > "tmp/file.log"` and then call the function, 
it returns "test". If we try again it goes away. So this function must be
cat'ing whatever is there then deleting the program

So if we create a symbolic link:
```bash
ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log
```
then run it, we get the output we wish (which is the password)





## 6 --> 7
another brute force:
```bash
#!/bin/bash
for i in {0000..9999}
do
	~/leviathan6 $i
done
```
(running this in parallel with '&' didn't work out, presumably because the
program changes the user in the current process only)
