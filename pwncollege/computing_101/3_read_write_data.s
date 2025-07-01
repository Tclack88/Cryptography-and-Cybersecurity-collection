; The culmination of the challenges here:
; https://pwn.college/computing-101/hello-hackers/
; reads data from stdin, storing it to memory address 1337000
; then writes that data from there to stdout, then exits
.intel_syntax noprefix
.global _start
_start:
        mov rdi,0
        mov rsi,1337000
        mov rdx,8
        mov rax,0
        syscall
        mov rdi,1
        mov rsi,1337000
        mov rdx,8
        mov rax,1
        syscall
        mov rdi, 42
        mov rax, 60
        syscall
