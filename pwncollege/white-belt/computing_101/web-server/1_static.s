// Building up from the last, this is a static server. In addition to the basic establishing connection, it will continue on in order to: read an incoming request (placing what is read onto the stack), write a response (a standard 200 OK), then close the connection  (these 3 commands are of course squeezed in before the exit syscall)
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

mov rdi, 4
sub rsp, 1024
mov rsi, rsp
mov rdx, 1024
mov rax, 0
syscall

mov rdi, 4
mov rsi, offset str
mov rdx, 19
mov rax, 1
syscall

mov rdi, 4
mov rax, 3
syscall

mov rax, 49
mov rdi, 0
mov rax, 60
syscall

.data
        str:
                .string  "HTTP/1.0 200 OK\r\n\r\n"
