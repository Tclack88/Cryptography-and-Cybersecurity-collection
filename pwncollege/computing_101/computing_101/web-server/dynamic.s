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

// read(4, <read_request>, <read_request_count>) = <read_request_result>
mov rdi, 4
sub rsp, 1024
mov rsi, rsp
mov rdx, 1024
mov rax, 0
syscall

mov r10, rax

// need to jump to find_space, save ret val to rbx (start), do again, save return val to rcx (end) then pass start and difference to "open" in next area
mov rdx, rsi
jmp find_first_space

find_first_space:
        inc rdx
        cmp BYTE PTR [rdx],32
        jne find_first_space
        inc rdx
        mov rbx, rdx

jmp find_second_space
find_second_space:
        inc rdx
        cmp BYTE PTR [rdx],32
        jne find_second_space
        mov rcx, rdx
        mov BYTE PTR [rdx], 0

// open("<open_path>", O_RDONLY) = 5
mov rdi, rbx
//add rdi, 32
mov rsi, 0
mov rdx, 0
mov rax, 2
syscall

// read(5, <read_file>, <read_file_count>) = <read_file_result>
mov rdi, 5
mov rsi, rsp
mov rdx, r10
mov rax, 0
syscall
// save rax (# of bytes from above) for write later
mov r10, rax


//close(5) = 0
mov rdi, 5
mov rax, 3
syscall

// write(4, "HTTP/1.0 200 OK\r\n\r\n", 19) = 19
mov rdi, 4
mov rsi, offset str
mov rdx, 19
mov rax, 1
syscall

// write(4, <write_file>, <write_file_count>) = <write_file_result>
// r10 stored buffer size, output of read above.
mov rdi, 4
mov rsi, rsp
mov rdx, r10
mov rax, 1
syscall

// close(4) = 0
mov rdi, 4
mov rax, 3
syscall

// exit(0)
mov rax, 49
mov rdi, 0
mov rax, 60
syscall

.data
        str:
                .string "HTTP/1.0 200 OK\r\n\r\n"
