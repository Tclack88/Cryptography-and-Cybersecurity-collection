// Example of averaging numbers stored consecutively in a for-loop 
.intel_syntax noprefix
mov rax, 0
mov rbx, 0
my_loop:
        add rax, [rdi+rbx*8]
        add rbx, 1
        cmp rbx, rsi
        jne my_loop
end:
        div rsi
