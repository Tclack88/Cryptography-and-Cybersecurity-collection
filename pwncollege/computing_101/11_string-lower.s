.intel_syntax noprefix
mov rbx,0
cmp byte ptr [rdi], 0
je leave
loop:
cmp byte ptr [rdi], 0
je leave
cmp byte ptr [rdi], 0x5a
jg skip_foo
push rdi
movzx rdi, byte ptr [rdi]
call 0x403000
pop rdi
mov byte ptr [rdi], al
inc rbx
skip_foo:
inc rdi
jmp loop
leave:
mov rax, rbx
