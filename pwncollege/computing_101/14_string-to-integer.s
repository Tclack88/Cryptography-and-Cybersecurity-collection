#Purpose, two digit number (string) is passed into here, we convert to actual number and return. This is basically the atoi function and is named as such
.intel_syntax noprefix
.global atoi_digit
.global atoi
atoi_digit:
movzx rax, BYTE PTR [rdi]
sub rax, 0x30
ret

atoi:
mov rdx,0
mov rcx,0
loop:
imul rdx,10
push rdi
lea rdi, BYTE PTR [rdi+rcx]
call atoi_digit
pop rdi
add rdx, rax
inc rcx
cmp BYTE PTR [rdi+rcx],0
jne loop

exit:
mov rax, rdx
ret
