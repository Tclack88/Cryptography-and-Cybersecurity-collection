# Playing With Programs
notes and lessons learned
## Dealing With Data
- Can read the hex content of a file with `xxd ps <file.txt>` xxd for "hexdump". To make it continuous as the computer actually sees, you can view it as plain with the `-ps` flag
- Reverse this with the `-r` flag `echo 68690a | xxd -ps -r` prints "hi" (with a newline)
- terminate input (from a read) without a new line: press `<ctrl-d>` instead of `<enter>`

## Talking Web
- General points of confusion addressed
	- "Host" (the server's name). below in `nc`,`curl` and python's request library, we will be connecting to an ip and at may be specifying a host name. It seems unnecessary if we have the ip address (DNS servers usually do ip lookups to find the host). Why would we need it? Virtual hosting. A company with many websites can host them all on a single machine with a single ip address
- nc:
	- `nc hostname port` to connect remotely
	- send an HTTP request after connecting. eg: `GET / HTTP/1.0`
	- Any more details in the request, can be added after this eg.
	```
	GET / HTTP/1.0
	Host: some-site.com
	```
	- Sending more args in your get request (query strings): `GET /?keyword=value HTTP/1.0`
	- sending multiply args in query string, just `&` separate: `GET /?key=abc&auth=123 HTTP/1.0`
	- POST request. eg:
	```
	nc "website.com" 80
	POST /path/to/form HTTP/1.0
	Host: website.com
	Content-Type: application/x-www-form-urlencoded
	Content-Length: 13 

	keyword=value
	```
	note: the empty newline after `Content-Length` is necessary, it bridges to the actual content
	- The content can be placed into a file ant then redirected. eg.
	`nc "website.com" 80  < post_content.txt` (`post_content.txt` here contains everything accept the top `nc`-calling line
	- Sending multiple values in a post: Since it's a post, not a get, we can't put the content as a query string, it goes in the botton. Must be on one line (eg. `key1=val1&key2=val2`)
	- redirects: A 300-response (3xx) will be returned and must manually be followed.
	  - providing redirects as a server. Put it in a header and have netcat listen with that input: (`nc -l -N <port> < <response_file>` (note: -N closes the content immediately once a response is received.
	  response_file:
	  ```
	  HTTP/1.1 301 Moved Permanently
	  Host: challenge.localhost
	  Location: http://challenge.localhost/attempt
	  Connection: close
	  ```
	- cookies: the response would usually display the cookie set (can just do a `HEAD` instead of `GET` request). But toinclude a previous session's cookies add `Cookie: <name>=<value>` to the header (not `Set-Cookie: ...`. Think of this not meaning "set this cookie value to be...", rather, "this cookie was set to...", or "this is what the cookie was set to")
- curl:
	- netcat is general, curl is specifically made for HTTP, so explicit GET / HTTP/1.0 isn't required
	- use `-A "Firefox"` flag to impersonate the user agent
	- Alternatively, more generally `-H "User-Agent: Firefox"` can be used any headers
	- `-I`/`-i` (for "Include")  flag will return only the response headers (which is weird because "include" sounds like it should add an additional thing). eg. `curl "http://somewebsite.com" -I` may return:
	```
	HTTP/1.1 200 OK
	Server: Werkzeug/3.0.6 Python/3.8.10
	Date: Thu, 01 Jan 2026 18:58:50 GMT
	Content-Type: text/html; charset=utf-8
	Content-Length: 84
	Connection: close
	```
	- `-v` (verbose) will display those headers AND the content
	```
	IPv6: :: 1
	(more items)
	HTTP/1.1 200 OK
    Server: Werkzeug/3.0.6 Python/3.8.10
    Date: Thu, 01 Jan 2026 18:58:50 GMT
    Content-Type: text/html; charset=utf-8
    Content-Length: 84
	Connection: close
	<html><head><title>Website Title</title></head><body><h1>content!</h1></body></html>
    ```
	- Sending more args in your get request (query strings): `curl "website.com" -G -d "keyword=value"` `-G` specifies get and `-d` is for data.
	- multiple values in query string, edit the content with `&` as separator as: `-G -d "pin=123&key=abc"`. Alternatively, it can just be included in query string, but with escaped `&`'s (`curl website.com/asset?pin=123\&key=abc`)
	- POST: just remove the `-G` flag and retain the data `-d`: `curl "website.com" -d "keyword=value"` can optionally explicitly add `-X POST`: `curl -d "keyword=value" -X POST website.com`
	- redirects: `-L` flag will automatically follow the redirect
	- cookies:
	  - To save all cookies after session ends, use `-c <filename>` (`-c` short for `--cookie-jar`)
	  - To append cookies from a previous sesstion, use `-b COOKIE=VAL;COOKIE2=VAL2` (no easy way to remember `-b`, it's "short" for `--cookie`. idk, maybe it's cookies you're `b`ringing?)
- python requests library
	- 	```
	  	import requests
		host = "http://url/goes/here" # no port required
		resp = requests.get(host)
		print(resp.text)
		```
	- add headers:  `requests.get(host, headers={"Host":"google.com"})` These headers can fool the server regarding which hostname the request is for
	- Sending more args in your get request (query strings): `requests.get(url, params={"keyword":"value"})`
	- POST request (similar to query strings, but change `params` to `data` 
		```
	  	import requests
		host = "http://url/goes/here"
		resp = requests.post(host, data={"keyword":"value"})
		print(resp.text)
		```
	- redirects: taken care of automatically by requests library
	- cookies: These are created in sessions, a single TCP connection that remains open. Requests library by default will open a connetion, do it's GET/POST/whatever requests, then close, so any cookies that are set are dropped. You can instead use `requests.Session` which will maintain the connection and thus any cookies or other things that need to remain set like authentication.
	```python
	import requests
	s = requests.Session()
	resp = s.get("http://localhost")
	print(resp.text)
	```
## program misuse
Some notes about various utilities (Lots of others probably here on [GTFObins](https://gtfobins.org/)):
 - `od` : octal dump. converts to octal characters. You can also display alongside the characters with the `-c` flag `od -c filename` might give something like: 
 ```
 0000000   h   e   l   l   o   -   f   r   i   e   n   d  \n
 ```
 (We can remove those spaces with tr: `od -c myfile | tr -d ' '`. This might remove intentional spaces though)
 - `hd` hex dump (characters are displayed by default)
 - `xxd` also hex dump, but allows the reverse. For instance `xxd my file | xxd -r` will display the file contents
 - `base32` and `base64`. convert to and from the repsective bases. Both have a `-d` option allowing for reversal of input like the piping just shown in `xxd`
 - `split` Allows for splitting contents from a file into multiple, eg by bytes `split myfile -b 5` might give:
 	```
	xaa <--filename
	  hello
	xab
	  -frie
	xac
	  -nd
	```
 - `gzip` compress a file (uncompressed with `gunzip`) (`gzip -c file > file.gz`)
 - `bzip2` similarly `bzip2 -c file > file.bz` and `bunzip2` is used for decompression
 - `zip`. Slightly more confusing `zip file.zip file`. It's backwards (add `-r` to make it recursiven and works for directories)
 - `tar` ("tape archive"). Used to bring many files together to archive (though tar doesn't do compression, that's usually done with gzip or bzip2 and they're often done together). eg. Archiving a file is: `tar -cvf file.tar file` (**c**reate, **v**erbose, **f**ile). Unarchiving is `tar - xvf file.tar` (e**x**tract). That retains the original file permissions however. You can print the output to stdout instead of to the files with the `-O` flag (`tar -xvf file.tar -O`). Alternatively, some things can read the raw binary (since tarballs themselves are not compressed) `more` does this. You can also view it during the compression `tar -cf - file | cat` (the hyphen `-` here instead of a file name indicates stdout)
 - `ar` Also archiving. Create an archive: `ar -r archive.a file` (`r` is for replace, which doubles as the adding/updating call). Extraction done with `ar -x archive.a` 
 - `cpio` Another archiver. This one is weird. The input comes from find, ls, echo. etc., just a string with the file name or path. And it needs a redirect to the file archive `echo filename | cpio -o > filename.cpio` (`o` is for "copy **o**ut I guess). But actually, not specifying an output file will actually print the contents (with other stuff) to stdout `echo filename | cpio -o`. Extracting seems to place it in it's own location, rather than making a copied archive, which is not as useful (`-i` flag)
