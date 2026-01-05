# Playing With Programs
notes and lessons learned
## Dealing With Data
- Can read the hex content of a file with `xxd ps <file.txt>` xxd for "hexdump". To make it continuous as the computer actually sees, you can view it as plain with the `-ps` flag
- Reverse this with the `-r` flag `echo 68690a | xxd -ps -r` prints "hi" (with a newline)
- terminate input (from a read) without a new line: press `<ctrl-d>` instead of `<enter>`

## Talking Web
- nc:
	- `nc hostname port` to connet remotely
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
	- Sending more args in your get request (query strings): `curl "website.com" -G -d "keyword=value"` `-G` specifies get and `-d` is for data
	- POST: just remove the `-G` flag and retain the data `-d`: `curl "website.com" -d "keyword=value"` can optionally explicitly add `-X POST`: `curl -d "keyword=value" -X POST website.com`
- python requests library
	- 	```
	  	import requests
		host = "http://url/goes/here" # no port required
		resp = requests.get(host)
		print(resp.text)
		```
	- add headers:  `requests.get(host, headers={"Host":"google.com"})` These headers can fool the server regarding which hostname the request is for
	- Sending more args in your get request (query strings): `requests.get(url, params={"keyword":"value"})`
	- multiple values in query string, edit the content with `&` as separator as: `-G -d "pin=123&key=abc"`
	- POST request (similar to query strings, but change `params` to `data` 
		```
	  	import requests
		host = "http://url/goes/here"
		resp = requests.post(host, data={"keyword":"value"})
		print(resp.text)
		```
