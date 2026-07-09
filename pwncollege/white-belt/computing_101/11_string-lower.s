// This is a segment of a function (as a result it must have a ret (LESSON LEARNED!). We must implement the following C code which calls another function foo. Another lesson learned: Even though the absolute address of the function foo was provided, do not call it directly, instead, push to a register and call that register
/*
str_lower(src_addr):
  i = 0
  if src_addr != 0:
    while [src_addr] != 0x00:
      if [src_addr] <= 0x5a:
        [src_addr] = foo([src_addr])
        i += 1
      src_addr += 1
  return i
*/
.intel_syntax noprefix
mov rbx,0
cmp rdi, 0
je leave
loop:
cmp byte ptr [rdi], 0
je leave
cmp byte ptr [rdi], 0x5a
jg skip_foo
push rdi
movzx rdi, byte ptr [rdi]
mov rcx, 0x403000
call rcx
pop rdi
mov byte ptr [rdi], al
inc rbx
skip_foo:
inc rdi
jmp loop
leave:
mov rax, rbx
ret
