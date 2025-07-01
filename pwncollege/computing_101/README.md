# Computing 101

lessons learned while working through these modules:

## programming in assembly:

* assembly code usually ends with a .s extension
* compile with `as my-program.s -o my-program.o`
* use the linker program `ld` (**l**ink e**d**itor) with `ld myprogram.o -o exe`
* intel syntax is pretty, AT&T is horrific, to use it, you must include:
	* `.intel_syntax noprefix` 
* the linker will complain if you don't include where to "start". If absent, it just starts from the top of the code
* alternatively: compile withh gcc but specify we don't want to import standard libary. (Also it seems comments are not welcome) `gcc -nostdlib my-program.s -o my-program`
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
### memory
brackets like: `[rax]` or `[0x7ffffff]` means "treat" this as a memory address
`mov rax, 0x12345` <- this instruction will just take the literal value 0x12345 and store it in rax.

```asm
mov rax, 0x12345
mov rbx, [rax]
```
^This second line says "whatever value is stored at memory address `0x12345`, but it in rbx.

```asm
mov rax, 0x133337
mov [rax], rbx
```
^The second line here says: take the value stored in rbx and store it at memory address 0x133337.

```asm
sub rsp, 8
mov [rsp], rcx
```
^ this is equivalent to a push. We are moving the stack pointer up 8 bytes, then moving the value of rcx into where rsp points (because we're using `[rsp]`)

### reading and writing
One way to read from, write to and open files in c is to make a syscall. For reading and writing is:
```
n = read(0,buf,100);  // 0 means stdin
write(1,buf,n); // 1 for stdout (write(file_descriptor, memory_address, length))
int open(const char *pathname, int flags)
```

This assembly equivalent is more complex and requires more arguments. The syscall value for read is `0` and for write is `1`, open is `2`, so this is what we will need to load into `rax` before the syscall. However we also need to establish that we're taking in from stdin and putting to stdout and where we want to read/write to, then finall that we want to read 100 bytes.

(Arguments in order for a variety of sys calls go to: `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`... possible mnemonics: `Dizzi Dixie 89`, or you have dee **i**nitial, then the **s**econd, then dee e**x**tras, then you **c**ontinue on... seriously, is **8** or **9** still not enough?)

In assembly (avoiding the header stuff), this can be accomplished with:

```asm
mov rdi, 0 ; 0 = stdin file descriptor
mov rsi, rsp ; read from the stack pointer
mov rdx, 100 ; number of bytes to read
mov rax, 0 ; the syscall for read()
syscall
```
key point: 100 is the buffer size, it's not necessarily going to be filled. The number of bytes read is returned in rax, which is why this is what will be passed into write

```asm
mov rdi, 1 ; 1 = stdout file descriptor
mov rsi, rsp ; write data from stack
mov rdx, rax ; number of butes to write (I'm a little unsure of why it's rax)
mov rax, 1 ; syscall for write()
syscall
```

```asm
mov rdi, rsp ; read data onto stack
mov rsi, 0 ; flag 0 = "read only" *** notes below
mov rax, 2; syscall for open()
syscall
```
Other flags for open:  (more info [here](https://4xura.com/pwn/orw-open-read-write-pwn-a-sandbox-using-magic-gadgets/))
*	0 - read only
*	1 - write only
*	2 - read/write
*	0x40 - create (if doesn't exist)
* 	0x200 - trunctate file to zero-length (if it exists)
*	0x400 - append to end of file

## inspection

* `strace` tracks system calls

* gdb: I already know `run` and `break` commands, but `starti` will set a breakpoint at the very start of the program, before any instructions begin executing.


# Solutions
https://pwn.college/computing-101/hello-hackers/

**Writing Output** (writing a single char (stored in address 1337000) ):
```asm
mov rdi, 1
mov rsi, 1337000
mov rdx, 1
mov rax, 1
syscall
```
