Description:

1844: A wire is strung between Washington and Baltimore. Forty miles of copper. A man sits at one end and listens.

The message arrives in silence and signal. Four words.

"What hath God wrought."

175 years later, someone left this file on a server. It looks like a rant. You've probably read it before.

Read it again.

The flag format will be SVIBGR{something}




I noticed the large spaces and that they weren't the same. The hint also implied stuff sent over the wire and I believe the first message sent was that "what god hath wrought", so it was clearly a morse code hint. So I wrote some code to count the spaces. Saw 2,3,4. 3's are the least common, so those must be the word boundary and clearly the dit is shorter than the dah

```python
import re

infile = 'wire.txt'

content = ""
with open(infile) as f:
        for line in f:
                content += line

spaces = re.compile('\s+')
space_list = spaces.findall(content)
num_list = [len(s) for s in space_list]
#print(num_list)

mapping = {2:'.',4:'-',3:' '}

print(''.join([mapping[i] for i in num_list[:-1]]))
```


Output:

```
... ...- .. -... --. .-. .-.-.- -- ----- .-. ... ...-- ..--.- -.-. ----- -.. ...-- ..--.- .---- ... ..--.- -.-. ----- ----- .-.. ...-..-
```

This [online translator](https://morsecode.world/international/translator.html) showed the message was:

`SVIBGR.M0RS3#C0D3#1S#C00L#`

So I just made some guesses and changed to `SVIBGR{M0RS3_C0D3_1S_C00L}`

