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
