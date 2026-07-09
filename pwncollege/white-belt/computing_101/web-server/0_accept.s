// This is all that is needed to establish a connection. In order (system calls separated with spaces) it:
// Creates a socket, binds on that socket port 80 (0x50, but as a word in little endian, 0050 becomes 5000) and ip 0.0.0.0, listens, accepts response, and finally exits
.intel_syntax noprefix
.global _start
_start:
mov rdi, 2
mov rsi, 1
mov rdx, 0
mov rax, 41
syscall

mov rdi, 3
sub rsp, 8
mov word ptr [rsp], 2
mov word ptr [rsp+2], 0x5000
mov dword ptr [rsp+4], 0
mov rsi, rsp
mov rdx, 16
mov rax, 49
syscall

mov rdi, 3
mov rsi, 0
mov rax, 50
syscall

mov rdi, 3
mov rsi, 0
mov rdx, 0
mov rax, 43
syscall

mov rax, 49
mov rdi, 0
mov rax, 60
syscall
