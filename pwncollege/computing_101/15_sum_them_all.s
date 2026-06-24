# combines itoa and atoi. First reads in values as strings (positive and negative allowed), converts them to decimals, combines them, then the total is converted into a string which is printed. So it's an added I guess
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
mov rbx, 0
lea rdi, [rsp+8]
mov rcx, QWORD PTR [rsp]
dec rcx
add_loop:
cmp rcx,0
je exit
add rdi, 8
push rcx
push rdi

mov rdi, [rdi]
call atoi
add rbx, rax

pop rdi
pop rcx
dec rcx
jmp add_loop

exit:
mov rdi, rbx
mov rsi, rsp
call itoa
mov rdi, 1
mov rsi, rsp
mov rdx, rax
mov rax, 1
syscall

mov rax, 60
syscall
