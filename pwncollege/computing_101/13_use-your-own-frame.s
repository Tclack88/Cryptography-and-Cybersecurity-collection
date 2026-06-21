# Here, we needed to make space on the stack, zero it out, then count the unique bytes loaded to an address on rdi (with length rsi). The sticking points/lessons learned was the movzx... lines. I couldn't move them directly into rax for example, I needed to add them to a separate register during which I can specify a byte pointer. The count of the unique values is returned via rax

.intel_syntax noprefix
.global solve 
solve:
sub rsp, 256
mov rcx,0
clear:
mov BYTE PTR [rsp+rcx],0
inc rcx
cmp rcx,256
jne clear
mov rcx, 0
fill:
movzx rdx, BYTE PTR [rdi+rcx]
mov BYTE PTR [rsp+rdx],1
inc rcx
cmp rcx,rsi
jne fill
mov rcx,0
mov rax,0
count:
movzx rdx, BYTE PTR [rsp+rcx]
add rax, rdx
inc rcx
cmp rcx,256
jne count
exit:
add rsp,256
ret
