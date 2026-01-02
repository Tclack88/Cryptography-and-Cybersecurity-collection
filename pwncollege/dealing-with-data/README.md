# Playing With Programs
notes and lessons learned
## Dealing With Data
- Can read the hex content of a file with `xxd ps <file.txt>` xxd for "hexdump". To make it continuous as the computer actually sees, you can view it as plain with the `-ps` flag
- Reverse this with the `-r` flag `echo 68690a | xxd -ps -r` prints "hi" (with a newline)
- terminate input (from a read) without a new line: press `<ctrl-d>` instead of `<enter>`

## Talking Web
- curl:
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
