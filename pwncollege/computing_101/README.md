# Computing 101

lessons learned while working through these modules:

## programming in assembly:

* assembly code usually ends with a .s extension
* compile with `as my-program.s -o my-program.o`
* use the linker program `ld` (**l**ink e**d**itor) with `ld myprogram.o -o exe`
* intel syntax is pretty, AT&T is horrific, to use it, you must include:
	* `.intel_syntax noprefix` 
* the linker will complain if you don't include where to "start". If absent, it just starts from the top of the code
* syscalls are made by setting the number (into `rax`) then performing the `syscall` command. In particular with exit, the syscall is 60 and the return value is loaded into the `rdi` register

An example of a program that merely exits (with return value 42)

```asm
.intel_syntax noprefix
.global _start
_start:
	mov rdi, 42
	mov rax, 60
	syscall
```

## inspection

* `strace` tracks system calls

* gdb: I already know `run` and `break` commands, but `starti` will set a breakpoint at the very start of the program, before any instructions begin executing.
