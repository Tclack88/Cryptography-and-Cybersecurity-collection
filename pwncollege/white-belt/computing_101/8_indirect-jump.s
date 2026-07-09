// constraints: only one cmp, no more than 3 jumps of any type
// The C source code could be like a switch-case. 
// In the event that many values are being checked, rather than using many cmp
// followed by many je, jg, jl, etc, you make a table of values you will
// jump to in this case that table was stored at rsi. If rdi, is 1,2,3, etc
// you can jump to the desired location
.intel_syntax noprefix
cmp rdi, 3
jg default_case
jmp [rsi+rdi*8]
default_case:
jmp [rsi+32]
