// Speed = distance / time	
// Please compute the following:
// speed = distance / time, where:
// distance = rdi
// time = rsi
// speed = rax
.intel_syntax noprefix
.global _start
_start:
        mov rdx, 0
        mov rax, rdi
        div rsi
        mov rdi, rsi // note: exit included for proper program, but fails challenge
        mov rax, 60
        syscall
