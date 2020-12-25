# Lessons learned in hackthissite basic challenges
## 6: I can see an encryption

The encrypted key is:


putting in aaaaaaa gives:  abcdef <br>
putting in 9999999 gives:  9:;<=>?@A <br>
putting in ZZZZZZZ gives:  Z[\\]^\_\` <br>


It looks like this is an increment the first by 0, the next by 1, next by 2, etc. Possibly by ASCII order. Man ascii to get the order and count backward... or write a python script:

```python
enc = "a65:;7=?"
enc = list(enc)
solved = [chr(ord(e)-i) for i,e in enumerate(enc)]
print(''.join(solved))
```


7: output of a .pl (pearl) script, which gives the output of a unix command. This means there's osme interaction with the server, so I will add a "; ls"

```
index.php
level7.php
cal.pl
.
..
k1kh31b1n55h.php
```

Not sure why ";cat k1kh31b1n55h.php" does not show the contents, but it shows up when I add it to the url as "blahblah.com/k1kh31b1n55h.php" 



## Server Side Includes (SSI) Injection

.shtml is vulnerable to this. You can change the dynamic content of the page by adding in what looks like html comments of the form `<!--#directive cmd="cmd" --> `

directive/cmd pairs can include: echo-var,  include-virtual, exec-cmd

Gives server commands (need to know/guess the server because commands are different if Linux vs windows for example)

eg. `<!--#exec cmd="ls" -->`  (in windows, "ls" would be "dir" for example)
