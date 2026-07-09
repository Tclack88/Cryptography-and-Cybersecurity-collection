// This was an implementation of a C code where the most common byte was counted. I had a solution that seemed like it would work, however I was getting a memory error. An LLM made the suggestions which after time now makes sense. The necessary background is that the information stored starting at rdi, and every 2 bytes (dword) thereafter.
/*
most_common_byte(src_addr, size):
  i = 0
  while i <= size-1:
    curr_byte = [src_addr + i]
    [stack_base - curr_byte * 2] += 1
    i += 1

  b = 1
  max_freq = 0
  max_freq_byte = 0
  while b <= 0x100:
    if [stack_base - b * 2] > max_freq:
      max_freq = [stack_base - b * 2]
      max_freq_byte = b
    b += 1

  return max_freq_byte
*/
.intel_syntax noprefix
push rbp
mov rbp, rsp

sub rsp, 0x800             
mov rbx, 0
zero_loop:
mov rax, rbx
imul rax, -8               
mov qword ptr [rbp + rax], 0
inc rbx
cmp rbx, 0x100            
jl zero_loop

mov rbx, 0                
loop1:
mov rax, rsi
sub rax, 1                
cmp rbx, rsi
jg countinue           
mov al, byte ptr [rdi + rbx] ;  This is the key change. Previously I had "mov rax, [rdi + rbx]" 
imul rax, -8               
inc qword ptr [rbp + rax]       
inc rbx
jmp loop1
countinue:
mov rbx, 1               
mov rdi, 0               
mov rcx, 0               
loop2:
cmp rbx, 0x100
jg leave
mov rax, rbx
imul rax, -8
mov rax, [rbp + rax]
cmp rax, rcx
jle increment_b
mov rcx, rax
mov rdx, rbx            
increment_b:
inc rbx
jmp loop2
leave:
mov rax, rdx
mov rsp, rbp
pop rbp
ret
