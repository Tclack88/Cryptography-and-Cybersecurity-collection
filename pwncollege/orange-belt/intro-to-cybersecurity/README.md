# Intro To CyberSecurity

## Web Security
`curl --path-as-is`: curl normally squashes input like `../../etc/passwd` This avoids that

Valid command injection operators:

|name|operator|
---
|semicolon|;|
|newline|\n|
|background|&|
|pipe|\|
|and|&&|
|or|\|\||
|subshell|\`command-string\`|
|subshell|$(command-string)|

Other tricks:

 - Whitespaces. Can use tabs if spaces are blocked. URLs take `+` for spaces (eg. `curl+\flag`). `${IFS}` (internal field separator)
 - special characters, such as the list above. URLs can take ascii but with a percentage. eg newline 0x0a --> %0a

### XSS
Here's a fetch in javascript making a post request
```js
<script>
	const url ="http://somewhere.com";
	const options = {method:"POST"};
	fetch(url,options)
</script>
```
### Cross Site Forgerty Requests (CSFR)
 - Redirects preserve headers, so a simple get requests can be accomplished by setting a redirect. If it comes from the site of interest, then authentication cookies would still be present and there's no problems with Cross-Origin Request Sharing (CORS).
 - HTML predates JS (and their associated seurity rules) and so CORS restrictions do not apply there, for instance with forms (and a post request made from it)
 
## Intercepting Communication
 - subnetting. For an ip address eg. 192.168.10.0 (32 bits total), this is a particular device, the network (such as a school, home, etc) will have the same higher bits (32 bits total). Larger organizations need more devices and so allocate less for the subnet. The subnet is given by a mask of 1's. For instance `11111111.11111111.11111111.00000000` or `255.255.255.0` specifies the top 24 bits are all the network and the lower 8 bits can just be represented with a `/24`. So `192.168.10.4/24` for instance. This means this network can support 254 unique devices (not 256 as it 0-255, because the first and last, 0 and 255 are reserved for special purposes).
 - Scanning a port? Without nmap it can be done in bash:
 ```bash
 for i in $(seq 0 255); do
	ping -c 1 -q 10.0.0.$i; 
 done
 ```
 - `nmap` Scanning a large number of machines on a specific port can be done simply with `nmap ip.add.re.ss/16 -p port`. But to make it faster, you can do something like: `nmap ip.add.re.ss/16 -p port -n -Pn --min-rate 5000`
 	- `-n` **n**o DNS resolution. If you only care about raw ip addresses and not website they may represent
	- `-Pn` **n**o **p**ing/host discovery. nmap pings first to see if a host is online. A firewall may block it and nmap retries, wasting time, `Pn` assumes they're all active and just probes the port
	- `--min-rate <packets-per-sec>` Can easily be pushed to 10000 or perhaps higher in a local container/VM
	- Industry standard workflow is 2 stage. 1. discovery (as above), 2. targeted scan `nmap ip.add.re.ss -p port -A`
