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

`rax` is understood to be 64 bits, `ebx` is 32 bits. But some other memory address (`[0x40400]` for example), the data type there is uncertain. So if you want to add to their, you must specify what it is

```asm
mov qword ptr [0x40400], 0x1337 // qword (quad word is 64, it's a pointer)
```

That being said, a full `qword ptr` cannot be moved at once due to hardware limitations, but `dword ptr`, `word ptr`, `byte ptr` have no problems, dword ptrs can move over full 32 bytes, but qword ptrs cannot. Anything less than a dword can be moved over

```asm
mov byte ptr [rdi], 0xab 				; This is fine
mov word ptr [rdi], 0xabcd 				; This is fine
mov dword ptr [rdi], 0xaaaabbbb 		; This is fine
mov qword ptr [rdi], 0xaaaabbbbccccdddd ; NOT fine
mov qword ptr [rdi], 0xaaaabbbbcccc 	; NOT fine
mov qword ptr [rdi], 0xaaaabbbb		 	; NOT fine (still)
mov qword ptr [rdi], 0xaaaabbb		 	; This is fine
// How to do it? Use an intermediate:
mov qword ptr rax, 0xaaaabbbbccccdddd
mov [rdi], rax
```

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

### math
* `add reg1, reg2` is like reg1 += reg2 (reg1 and reg2 are added, results stored in reg1)
* `mul` vs `imul`: `mul` treats inputs as unsigned, `imul` (integer multiplication) treats them as signed, so it can take negative values. `mul` will treat negative numbers as their corresponding positive vals, eg. if reg1 = -1 and reg2 = 2, assuming an 8 bit register, where -1 in two's complement is `1111 1111` (255), `mul reg1, reg2` would be 255\* = 510. 
* `div` can divide a 128 bit dividend (numerator if represented by a fraction) by a 64 bit divisor (denominator). But our registers only hold 64 bits. So the number is formed by placing it into rdx, then rax. This is one single number, represented as `rdx:rax`. Of course, if dividing small numbers like 10/3, you can set `rdx` to zero (you MUST actually, otherwise junk data left over there will result in incorrect results), then the `10` (ten) gets placed into `rax`:
```asm
mov rdx,0
mov rax,10
mov reg, 3
div reg // result stored in rax with rdx holding remainder
// This last instruction is like:
rax = rdx:rax / reg // remainder not stored int rax (with 10/3, rax = 3)
rdx = remainder     // remainder stored here (with 10/3, rdx = 1)
```
See div solutions in `4_integer-division.s` and `5_modulo-operation.s` 
* although a mod can be cacluated with the `div` operator, it can be slow. A trick exists if doing `x % y` and `y` is a power of 2 (2^n), the result will be the lower n bits of x. eg. 143 / 4. 143 = `1000 1111`, 4 = `100`. The result would be `0010 0011.11`, where I write this `.11` as the remainder, it's remainder 3!. So those right two zeros (because 4 = 2^2) means I will "clear out" the right two binary digits of `x`, setting that as the remainder
* `shr` and `shl` are shifting operations (`shr rax, 3` would shift rax 3 bits (not bytes) right and replace rax with that new value)
* `and`, `or`, `not` and `xor` all work bitwise
* `cmp reg1, reg2`. If they are equal, it sets the zero flag to 1 (true), usually after this a jump is called (`je`, jump if equal will jump if that zero flag is indeed 1 or `jne`, jump if not equal if it's a 0). As with other instructions, like the `mov`, if specifying a register, you'll need to specify if it's dword, qword, etc.

### stack
The stack is the longer term memory store than the registers. Suitable for static data (as opposed to dynamic data such as that made with `malloc`, `realloc`, `calloc`, etc. and freed with... well `free`. This dynamic data goes on the heap is used for). You can put items on it with `push`, then pull them away with `pop`. Storing the value from pop is as simple as giving the register (eg. `pop rbx` takes the value on the top of the stack and aves it into `rbx`). Pushing is the opposing (`push rbx` will place whatever value is in rbx to the top of the stack)

### other stuff

* Jumping: Jumps generally aren't supported to directly allow jumping to immediate addresses, instead you have to load the address into a register, then call `jmp` on that register.
```asm
mov rax, 0x403000
jmp rax
// But this doesn't work:
jmp 0x403000
```
Jumps can be relative or to a label (which which is a symbol that's created at run time to represent an address of an instruction or data). It lives in its own memory address. After a jump goes there, the instruction immediately after it is then executed (i.e. it's not the address of the next instruction to be executed). See `6_relative-jump.s` for an example.

* `je`, `jl` etc. cannot be paired with relative addresses (`je [rsi+8]`, `je rax` (etc). You have to make a label. See `8_indirect-jump.s` as an example of using this via the idea of a jump table (used for switch statements with many possible values) and `9_average-loop.s` for another example of jne into a label

* If-else if-else with jumps. This logic can be done with a combination of labels and `cmp` along with `je` or `jne` statments. (eg given in `7_condtional-jump.s`)


## inspection

* See your decompiled code (with binary) with `objdump`: `objdump -M intel my-program` (`-M intel` overrides the default AT&T syntax
* To export just the binary (not the human-readable), use `objcopy`: `objcopy --dump-section .text=output_file_name my-program` (why .text? that's where the raw machine code is held. No headers, metadata or other sections included)
* `strace` tracks system calls
* gdb: I already know `run` and `break` commands, but `starti` will set a breakpoint at the very start of the program, before any instructions begin executing.
* How does this debugging break work? It's the same as including a single `int3` command:
```asm
mov rdi, 42
mov ra, 60
int3 ; triggers the debugger breakpoint, pausing execution
syscall
```


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
