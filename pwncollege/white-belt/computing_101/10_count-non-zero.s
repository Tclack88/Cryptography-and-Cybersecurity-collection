// counts number of non-zero BYTES starting from address at rdi
// (with count stored into rax variable)
.intel_syntax noprefix
mov rax, 0
cmp rdi, 0
je end
main_loop:
        mov rbx, [rdi+rax]
        cmp rbx, 0
        jne increment
jmp end
increment:
        add rax, 1
        jmp main_loop
end:
