# all the math problems in "computing 101" > "numbers as strings" > "math" > "unary operators". Unary operators contains all the previous ones, so it's a good penultimate sample to save. Input is either 3 values: "./progam num1 +/-/*/^/|/& num2" or 2 values "./program !/- num" and it gets computed and printed. Any other symbols will be rejected, exit with status 1.

.intel_syntax noprefix
.global itoa_digit
.global itoa
.global _start
.global atoi
.global atoi_digit

atoi_digit:
movzx rax, BYTE PTR [rdi]
sub rax, 0x30
ret
atoi:
mov rdx,0
mov rcx,0
cmp BYTE PTR [rdi],0x2d
jne atoi_loop
mov rcx,1
atoi_loop:
imul rdx,10
push rdi
lea rdi, BYTE PTR [rdi+rcx]
call atoi_digit
pop rdi
add rdx, rax
inc rcx
cmp BYTE PTR [rdi+rcx],0x39
ja exit_atoi
cmp BYTE PTR [rdi+rcx],0x30
jb exit_atoi
jmp atoi_loop 
exit_atoi:
mov rax, rdx
cmp BYTE PTR [rdi], 0x2d
jne done
neg rax
done:
ret 



itoa_digit:
add rdi, 0x30
mov rax, rdi
ret
itoa:
mov rax, rdi
mov rcx, 0
mov r10, 10
mov r11, 1
cmp rax, 0
jg stack
neg rax
mov r11, rdi
stack:
xor rdx, rdx
div r10

mov r8,rax
mov rdi, rdx
call itoa_digit
push rax
inc rcx
mov rax, r8
cmp rax,0
jne stack

mov r8,rcx
mov rdi, 0
cmp r11,0
jge unstack
push 0x2d
inc r8
inc rcx
unstack:
pop rax
mov BYTE PTR [rsi+rdi],al
dec rcx
inc rdi
cmp rcx,0
jne unstack

mov rax, r8
ret



_start:
cmp BYTE PTR [rsp],4
je math_ops

mov r13, [rsp+16]
mov r14, [rsp+24]
mov rdi, r14
call atoi
mov rbx, rax
mov rdi, 1
cmp BYTE PTR [r13], 0x2d
je neg_op
cmp BYTE PTR [r13], 0x7e
je not_op
jmp exit

math_ops:
mov rdi, 1
mov r12, [rsp+16]
mov r13, [rsp+24]
mov r14, [rsp+32]

mov rbx, 0
mov rdi, r12
call atoi
add rbx, rax
mov rdi, r14
call atoi

cmp BYTE PTR [r13], 0x2b
je add
cmp BYTE PTR [r13], 0x2d
je sub
cmp BYTE PTR [r13], 0x2a
je mul
cmp BYTE PTR [r13], 0x5e
je xor_op
cmp BYTE PTR [r13], 0x7c
je or_op
cmp BYTE PTR [r13], 0x26
je and_op

exit:
add rsp, 0x80
mov rax, 60
syscall

continue:
sub rsp, 0x80
mov rdi, rbx
mov rsi, rsp
call itoa

mov rdi, 1
mov rsi, rsp
mov rdx, rax
mov rax, 1
syscall
mov rdi, 0
jmp exit

add:
add rbx, rax
jmp continue

sub:
sub rbx, rax
jmp continue

mul:
imul rbx, rax
jmp continue

xor_op:
xor rbx, rax
jmp continue

or_op:
or rbx, rax
jmp continue

and_op:
and rbx, rax
jmp continue

neg_op:
neg rbx
jmp continue

not_op:
not rbx
jmp continue
