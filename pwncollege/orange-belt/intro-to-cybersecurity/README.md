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
