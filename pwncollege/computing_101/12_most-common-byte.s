// work in progress
.intel_syntax noprefix
mov rbx, 0
loop1:
mov rax, rsi
sub rax, 1
cmp rbx, rax
jg continue
mov rcx, [rdi+rbx]
inc [rbp-rcx*2]
jmp loop1
continue:
mov rbx, 1
mov rcx, 0
mov rdx, 0
loop2:
cmp rbx, 0x100
jg leave
mov rax, [rbp-rbx*2]
mov r8, rax
cmp r8, rcx
jle increment_b
mov rcx, r8
mov rdx, rbx
increment_b:
inc rbx
jmp loop2
leave:
mov rax, rdx
ret
