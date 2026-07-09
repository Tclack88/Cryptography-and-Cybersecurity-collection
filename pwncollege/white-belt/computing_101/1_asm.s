; the first few challenges of this page:
; https://pwn.college/computing-101/your-first-program/
; lead to building this program which just exits
; compile with "as asm.s -o asm.o" to make linker
; then  complete linker to executable with something like: "ld asm.o -o exe"
.intel_syntax noprefix
.global _start
_start:
mov rdi, 42
mov rax, 60
syscall
