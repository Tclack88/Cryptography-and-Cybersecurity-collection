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
