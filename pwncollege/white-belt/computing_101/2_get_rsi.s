; the last challenge of https://pwn.college/computing-101/your-first-program/
; wherein a "secret" value is red from rsi. It's moved into rdi as the exit code
; compile with "as get_rsi.s -o get_rsi.o" then "ld get_rsi.o -o exe"
.intel_syntax noprefix
.global _start
_start:
        mov rdi, rsi
        mov rax, 60
        syscall
