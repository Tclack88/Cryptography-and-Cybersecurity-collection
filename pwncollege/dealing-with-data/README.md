# Playing With Programs
notes and lessons learned
## Dealing With Data
- Can read the hex content of a file with `xxd ps <file.txt>` xxd for "hexdump". To make it continuous as the computer actually sees, you can view it as plain with the `-ps` flag
- Reverse this with the `-r` flag `echo 68690a | xxd -ps -r` prints "hi" (with a newline)
- terminate input (from a read) without a new line: press `<ctrl-d>` instead of `<enter>`
