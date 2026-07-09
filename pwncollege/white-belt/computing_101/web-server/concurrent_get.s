.intel_syntax noprefix
.global _start
_start:

//socket
mov rdi,2
mov rsi, 1
mov rdx, 0
mov rax, 41
syscall
//store socket fd to r14
mov r14, rax

//bind socket to port 80 on 0.0.0.0
mov rdi, r14
sub rsp, 16
mov WORD PTR [rsp], 2
mov WORD PTR [rsp+2], 0x5000
mov DWORD PTR [rsp+4], 0
mov QWORD PTR [rsp+8],0
lea rsi, [rsp]
mov rdx, 16
mov rax, 49
syscall
add rsp, 16

// listen
mov rdi, r14
mov rsi, 0
mov rax, 50
syscall

await_accept:

// accept (save fd of input to r15)
mov rdi, r14
mov rsi, 0
mov rdx, 0
mov rax, 43
syscall
mov r15, rax

// fork
mov rax, 57
syscall
cmp rax, 0
je child_process

// parent: close accept
mov rdi, r15
mov rax, 3
syscall
jmp await_accept

  //handle child process
  child_process:

  // child: close socket (r14) (why? does this not affect the traffic/response?)
  mov rdi, r14
  mov rax, 3
  syscall

   // child: read text content from client
  mov rdi, r15
  sub rsp, 1024
  mov rsi, rsp
  mov rdx, 1024
  mov rax, 0
  syscall

  // get filename location from string (store addr on rsp-16 and len on rsp-8)
  lea rdi, [rsp]
  call get_filename

  // child: open file
  mov rdi, rax
  mov rsi, 0
  mov rax, 2
  syscall
  // store file's fd in r13
  mov r13, rax

  // child: read file content, save output length on stack, needed when writing content
  mov rdi, r13
  mov rsi, rsp
  mov rax, 0
  syscall
  push rax

  // child: close file
  mov rdi, r13
  mov rax, 3
  syscall

  // child: write "OK" to client
  mov rdi, r15
  lea rsi, [rip+ok_response]
  mov rdx, 19
  mov rax, 1
  syscall

  // child: write file content to socket
  pop rdx
  mov rdi, r15
  mov rsi, rsp
  mov rax, 1
  syscall

  // child: clean up stack memory allocated when reading text from client
  add rsp, 1024
  // child: close connection with client
  mov rdi, r15
  mov rax, 3
  syscall

  // child: exits
  mov rdi, 0
  mov rax, 60
  syscall


ok_response:
  .ascii "HTTP/1.0 200 OK\r\n\r\n"

get_filename:
// expected input on rdi: "GET <location> <maybe-something-else-who-cares>"
// use r11 to find first space and r12 to find 2nd space (they will holding byte values for each char)
mov rcx,-1
first:
inc rcx
movzx r11, BYTE PTR [rdi+rcx]
cmp r11, 0x20
jne first
// now use r11 now to store (relative) location of string start
mov r11, rcx
inc r11
second:
inc rcx
movzx r12, BYTE PTR[rdi+rcx]
cmp r12, 0x20
jne second
// return starting address in rax, null terminate 2nd space location so read will naturally stop
lea rax, QWORD PTR [rdi+r11]
mov BYTE PTR [rdi+rcx], 0
ret
