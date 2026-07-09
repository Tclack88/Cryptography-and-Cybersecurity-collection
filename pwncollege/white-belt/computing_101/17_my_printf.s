# a copy of printf sort of (inherits the itoa and atoi logic from the math/calculator challenge)

.intel_syntax noprefix
.global _start

_start:
mov rcx, [rsp+16]
mov r9, 24
next_char:
cmp BYTE PTR [rcx],0
je exit
cmp BYTE PTR [rcx],0x5c
je escape_seq
cmp BYTE PTR [rcx],'%'
je format_seq
jmp write
continue:
inc rcx
jmp next_char

write:
push rcx ;write syscall clobbers rcx and r11, must preserve
mov rdi, 1
mov rsi, rcx
mov rdx, 1
mov rax, 1
syscall
pop rcx
jmp continue

write_number:
push rcx
add r9, 8

mov rdi, [rsp+r9]
call atoi

sub rsp, 0x80
mov rdi, rax
mov rsi, rsp
call itoa

mov rdi,1
mov rsi,rsp
mov rdx, rax
mov rax, 1
syscall

add rsp, 0x80
pop rcx
inc rcx
jmp continue

write_string:
push rcx
add r9,8
mov rcx, 0
mov rsi, [rsp+r9]
find_null:
cmp BYTE PTR [rsi+rcx],0
je write_return
inc rcx
jmp find_null
write_return:
mov rdi, 1
mov rdx, rcx
mov rax, 1
syscall
pop rcx
inc rcx
jmp continue

print_hex:
add rcx,2

movzx rdi, BYTE PTR [rcx]
call hex_helper 
mov r12, rax
inc rcx
movzx rdi, BYTE PTR [rcx]
call hex_helper
mov r14, rax

shl r12, 4
or r12, r14

push rcx
push r12
mov rdi,1
mov rsi, rsp
mov rdx,1
mov rax, 1
syscall
pop r12
pop rcx

jmp continue


exit:
mov rdi, 0
mov rax, 60
syscall

escape_seq:
cmp BYTE PTR [rcx+1],'n'
je newline
cmp BYTE PTR [rcx+1],'x'
je print_hex
cmp BYTE PTR [rcx+1],0x5c
jne continue
leave_escape:
inc rcx
jmp write

format_seq:
cmp BYTE PTR [rcx+1],'d'
je write_number
cmp BYTE PTR [rcx+1],'s'
je write_string
cmp BYTE PTR [rcx+1],'%'
jne continue
inc rcx
jmp write


newline:
mov BYTE PTR [rcx+1],0xa
jmp leave_escape

hex_helper:
mov rax, rdi
cmp rax,'A'
jge cap_case
cmp rax,'9'
jle num_case
sub rax, 'a'
add rax, 10
ret
cap_case:
sub rax,'A'
add rax,10
ret
num_case:
sub rax,'0'
ret



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
jne atoi_done
neg rax
atoi_done:
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


