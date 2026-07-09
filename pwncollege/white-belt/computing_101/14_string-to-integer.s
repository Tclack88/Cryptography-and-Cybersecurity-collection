#Purpose, two digit number (string) is passed into here, we convert to actual number and return. This is basically the atoi function and is named as such. It now takes into account negative numbers and ignores numeric values (eg 125A will just read 125 and then stop) 
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
cmp BYTE PTR [rdi],0x2d
jne loop
mov rcx,1

loop:
imul rdx,10
push rdi
lea rdi, BYTE PTR [rdi+rcx]
call atoi_digit
pop rdi
add rdx, rax
inc rcx
cmp BYTE PTR [rdi+rcx],0x39
ja exit
cmp BYTE PTR [rdi+rcx],0x30
jb exit
jmp loop

exit:
mov rax, rdx
cmp BYTE PTR [rdi], 0x2d
jne done
neg rax
done:
ret
