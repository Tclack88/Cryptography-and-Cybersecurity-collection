// This code is essentially jumping to a an address 0x51 instructions away. We need to fill it in with something to avoid entering some other section (beyond the .text section), so we fill it with nops. the .rept directive allows us to do that without writing forever
.intel_syntax noprefix
jmp target
.rept 0x51
nop
.endr
target:
mov rax, 1
