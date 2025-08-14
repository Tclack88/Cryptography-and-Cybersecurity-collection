// determine rdi % rsi
.intel_syntax noprefix
.global _start
_start:
        mov rdx,0
        mov rax, rdi
        div rsi
        mov rax, rdx // remainder stored in rdx from div. Move to rax
		mov rdi, 42
		mov rax, 60
		syscall
