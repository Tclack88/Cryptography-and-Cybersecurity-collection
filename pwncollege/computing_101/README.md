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
mov rdx, rax ; number of bytes to write (I'm a little unsure of why it's rax)
mov rax, 1 ; syscall for write()
syscall
```

```asm
mov rdi, rsp ; read data onto stack
mov rsi, 0 ; flag 0 = "read only" *** notes below
mov rax, 2; syscall for open()
syscall
```
Other flags for open:  (more info [here (all flags)](https://x64.syscall.sh/) and [here (ORW exploits)](https://4xura.com/pwn/orw-open-read-write-pwn-a-sandbox-using-magic-gadgets/))
*	0 - read only
*	1 - write only
*	2 - read/write
*	0x40 - create (if doesn't exist)
* 	0x200 - trunctate file to zero-length (if it exists)
*	0x400 - append to end of file

### math
https://x64.syscall.sh/https://x64.syscall.sh/* `add reg1, reg2` is like reg1 += reg2 (reg1 and reg2 are added, results stored in reg1)
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

[debugging refresher](https://pwn.college/computing-101/debugging-refresher/)
level 4
```asm
0x621ec554ed1b <main+629>       je     0x621ec554ed27 <main+641>           
0x621ec554ec55 <main+431>       call   0x621ec554e190 <puts@plt>           
0x621ec554ec5a <main+436>       lea    rdi,[rip+0xde7]        # 0x621ec554 
0x621ec554ec61 <main+443>       call   0x621ec554e190 <puts@plt>           
0x621ec554ec66 <main+448>       lea    rdi,[rip+0xe4f]        # 0x621ec554 
0x621ec554ec6d <main+455>       call   0x621ec554e190 <puts@plt>           
0x621ec554ec72 <main+460>       int3                                       
0x621ec554ec73 <main+461>       nop                                        
0x621ec554ec74 <main+462>       mov    DWORD PTR [rbp-0x1c],0x0            
0x621ec554ec7b <main+469>       jmp    0x621ec554ed2b <main+645>           
0x621ec554ec80 <main+474>       mov    esi,0x0                             
0x621ec554ec85 <main+479>       lea    rdi,[rip+0xe3c]        # 0x621ec554 
0x621ec554ec8c <main+486>       mov    eax,0x0                             
0x621ec554ec91 <main+491>       call   0x621ec554e250 <open@plt>
.
.
.
0x621ec554ed2b <main+645>       cmp    DWORD PTR [rbp-0x1c],0x3
0x621ec554ed2f <main+649>       jle    0x621ec554ec80 <main+474>           
0x621ec554ed35 <main+655>       mov    eax,0x0 
0x621ec554ed3a <main+660>       call   0x621ec554e97d <win>
0x621ec554ed3f <main+665>       mov    eax,0x0 
```
In this challenge, a random value is loaded and we are supposed to figure it out. Or.... I can see in the beginning (main+462) we load 0 into `rbp-0x1c` then compare that to 3, if it's less than or equal, we jump into the random value assignment, otherwise we call a `win` function which seems all too obvious to ignore. I can set that value with `set {int} ($rbp-0x1c) = 0x5`

level 5

Checking out the relevant part of main:
```
   0x00005976efc7ad33 <+653>:   nop
   0x00005976efc7ad34 <+654>:   mov    DWORD PTR [rbp-0x1c],0x0
   0x00005976efc7ad3b <+661>:   jmp    0x5976efc7adeb <main+837>
   0x00005976efc7ad40 <+666>:   mov    esi,0x0
   0x00005976efc7ad45 <+671>:   lea    rdi,[rip+0xd5e]        # 0x5976efc7baaa
   0x00005976efc7ad4c <+678>:   mov    eax,0x0
   0x00005976efc7ad51 <+683>:   call   0x5976efc7a250 <open@plt>
   0x00005976efc7ad56 <+688>:   mov    ecx,eax
   0x00005976efc7ad58 <+690>:   lea    rax,[rbp-0x18]
   0x00005976efc7ad5c <+694>:   mov    edx,0x8
   0x00005976efc7ad61 <+699>:   mov    rsi,rax
   0x00005976efc7ad64 <+702>:   mov    edi,ecx
   0x00005976efc7ad66 <+704>:   call   0x5976efc7a210 <read@plt>
   0x00005976efc7ad6b <+709>:   lea    rdi,[rip+0xd46]        # 0x5976efc7bab8
   0x00005976efc7ad72 <+716>:   call   0x5976efc7a190 <puts@plt>
   0x00005976efc7ad77 <+721>:   lea    rdi,[rip+0xd5a]        # 0x5976efc7bad8
   0x00005976efc7ad7e <+728>:   mov    eax,0x0
   0x00005976efc7ad83 <+733>:   call   0x5976efc7a1d0 <printf@plt>
   0x00005976efc7ad88 <+738>:   lea    rax,[rbp-0x10]
   0x00005976efc7ad8c <+742>:   mov    rsi,rax
   0x00005976efc7ad8f <+745>:   lea    rdi,[rip+0xd51]        # 0x5976efc7bae7
   0x00005976efc7ad96 <+752>:   mov    eax,0x0
   0x00005976efc7ad9b <+757>:   call   0x5976efc7a260 <__isoc99_scanf@plt>
   0x00005976efc7ada0 <+762>:   mov    rax,QWORD PTR [rbp-0x10]
   0x00005976efc7ada4 <+766>:   mov    rsi,rax
   0x00005976efc7ada7 <+769>:   lea    rdi,[rip+0xd3e]        # 0x5976efc7baec
   0x00005976efc7adae <+776>:   mov    eax,0x0
   0x00005976efc7adb3 <+781>:   call   0x5976efc7a1d0 <printf@plt>
   0x00005976efc7adb8 <+786>:   mov    rax,QWORD PTR [rbp-0x18]
   0x00005976efc7adbc <+790>:   mov    rsi,rax
   0x00005976efc7adbf <+793>:   lea    rdi,[rip+0xd37]        # 0x5976efc7bafd
   0x00005976efc7adc6 <+800>:   mov    eax,0x0
   0x00005976efc7adcb <+805>:   call   0x5976efc7a1d0 <printf@plt>
   0x00005976efc7add0 <+810>:   mov    rdx,QWORD PTR [rbp-0x10]
   0x00005976efc7add4 <+814>:   mov    rax,QWORD PTR [rbp-0x18]
   0x00005976efc7add8 <+818>:   cmp    rdx,rax
   0x00005976efc7addb <+821>:   je     0x5976efc7ade7 <main+833>
   0x00005976efc7addd <+823>:   mov    edi,0x1
   0x00005976efc7ade2 <+828>:   call   0x5976efc7a280 <exit@plt>
   0x00005976efc7ade7 <+833>:   add    DWORD PTR [rbp-0x1c],0x1
   0x00005976efc7adeb <+837>:   cmp    DWORD PTR [rbp-0x1c],0x7
   0x00005976efc7adef <+841>:   jle    0x5976efc7ad40 <main+666>
   0x00005976efc7adf5 <+847>:   mov    eax,0x0
   0x00005976efc7adfa <+852>:   call   0x5976efc7a97d <win>
   0x00005976efc7adff <+857>:   mov    eax,0x0
   0x00005976efc7ae04 <+862>:   mov    rcx,QWORD PTR [rbp-0x8]
   0x00005976efc7ae08 <+866>:   xor    rcx,QWORD PTR fs:0x28
   0x00005976efc7ae11 <+875>:   je     0x5976efc7ae18 <main+882>
   0x00005976efc7ae13 <+877>:   call   0x5976efc7a1c0 <__stack_chk_fail@plt>
   0x00005976efc7ae18 <+882>:   leave
   0x00005976efc7ae19 <+883>:   ret
```
What happens in this code is that a value is randomly assigned from /dev/random and we have to guess it, as before, but after properly guessing, a counter is incremented until 7 is reached. So we could manually read that value each time at a breakpoint, or use some scripting (which normally would be run with `gdb -x my_script.gdb mycode.out`, however in this challenge, gdb is initialized. So from gdb, we can run it just by using `source my_script.gdb`)

At main+757, the `scanf` function is called, so I figured we can jump to main+818 where the compare is made between `rdx` and `rax`
```gdb
set disassembly-flavor intel
break *main+757
commands
        set  $rip=main+818
        set  $rdx = 1
        set  $rax = 1
        continue
end

run
continue
```

of course, we could simply jump to the "win" condition `set $rip=*main+852` then continue from there, but that's no fun

## Building a Web Server
Socket System call accepts 3 arguments:
* domain (eg. `AF_INET` for ipv4) (int)
* type (eg. `SOCK_STREAM` for TCP) (int)
* protocol (usually set to 0) (int) 

A bind call accepts 3 arguments:
* sockfd (socket file descriptor, matches first arg in socket) (int)
* `struct sockaddr_in` (ptr to address)
* `socklen_t addrlen` (int)
bind is necessary because socket exists in a namespace, but it has no address assigned to it without bind

Listen accepts two arguements:
* sockfd (int)
* backlog (int)

Accept takes 3 arguments:
* sockfd (int)
* `struct sockaddr` (ptr to addr)
* `socklen_t` (ptr to addr length)

### Declaring and referecing variables in assembly:

If you want to write a string (which happens in this web server challenge, but also elsewhere). You can place the string to be written in the data section, and it can be moved directly to a variable (it would function as a pointer). Importantly, it will be a relative address, so the `offset` keyword must be used. Here's an example where a write is called and the pointer to the string being written is placed into rsi:

```asm
(some other code)

mov rdi, 4
mov rsi, offset str
mov rdx, 19
mov rax, 1
syscall

(some other code)

.data
     str:
          .string <blah blah>
```
