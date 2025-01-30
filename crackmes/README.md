#CRACKMEs
sourced from UCI course (shared with me). But it appears to come from Radare's crackme/tutorial [here](https://book.rada.re/crackmes/ioli/intro.html)

##crackme0x00
Intry/guided
`gdb ./crackme0x00` to open it. run `r` we are prompted for a password. Before moving further (the program would just exit with a likely incorrect guess), we can cancel causing a SIGINT. This would let us perform a backtrace (aliased `bt`) to see the callstack. This doesn't work if we incorrectly guess and the program exits because it exits cleanly and can't capture the stack trace. Whereas a SIGINT passes control back to gdb with the state it was just in.
```
IOLI Crackme Level 0x00
Password: ^C
Program received signal SIGINT, Interrupt.
0xf7fc4549 in __kernel_vsyscall ()
(gdb) bt
#0  0xf7fc4549 in __kernel_vsyscall ()
#1  0xf7e871a7 in read () from /lib/i386-linux-gnu/libc.so.6
#2  0xf7dfb876 in _IO_file_underflow () from /lib/i386-linux-gnu/libc.so.6
#3  0xf7dfca30 in _IO_default_uflow () from /lib/i386-linux-gnu/libc.so.6
#4  0xf7dd6ee9 in ?? () from /lib/i386-linux-gnu/libc.so.6
#5  0xf7dd4c09 in scanf () from /lib/i386-linux-gnu/libc.so.6
#6  0x0804845b in main ()
```
We can set a breakpoint at this point in main (all the other points like scanf are inaccessible) `tbreak *0x0804845b`. We can continue `c` undoing our interruption. Then disasemble our local operation with `disas`. Here are relevant lines before and after:
```
   0x08048443 <+47>:    call   0x8048340 <printf@plt>
   0x08048448 <+52>:    lea    eax,[ebp-0x18]
   0x0804844b <+55>:    mov    DWORD PTR [esp+0x4],eax
   0x0804844f <+59>:    mov    DWORD PTR [esp],0x804858c
   0x08048456 <+66>:    call   0x8048330 <scanf@plt>
=> 0x0804845b <+71>:    lea    eax,[ebp-0x18]
   0x0804845e <+74>:    mov    DWORD PTR [esp+0x4],0x804858f
   0x08048466 <+82>:    mov    DWORD PTR [esp],eax
   0x08048469 <+85>:    call   0x8048350 <strcmp@plt>
```
we can see the call to printf at the top, presumably asking for the password, some setup then the call to scanf where our password was being read then value returned and saved into address at `0x0804845b <+71>`. A call to strcmp will be made to eax and esp+0x4. So the stored password must be there. Which we can examine with `(gdb) x/s 0x804858f
0x804858f:      "250382"` 

NOTE: it's also found by inspecting the program with strings: `strings crackme0x00`. Somewhere in the middle we find this:
```
IOLI Crackme Level 0x00
Password:
250382
Invalid Password!
Password OK :)
```

##crackme0x01
Much the same. My dump of the assembly shows:
```
   0x08048413 <+47>:    call   0x804831c <printf@plt>
   0x08048418 <+52>:    lea    eax,[ebp-0x4]
   0x0804841b <+55>:    mov    DWORD PTR [esp+0x4],eax
   0x0804841f <+59>:    mov    DWORD PTR [esp],0x804854c
   0x08048426 <+66>:    call   0x804830c <scanf@plt>
=> 0x0804842b <+71>:    cmp    DWORD PTR [ebp-0x4],0x149a
   0x08048432 <+78>:    je     0x8048442 <main+94>
   0x08048434 <+80>:    mov    DWORD PTR [esp],0x804854f
   0x0804843b <+87>:    call   0x804831c <printf@plt>
   0x08048440 <+92>:    jmp    0x804844e <main+106>
   0x08048442 <+94>:    mov    DWORD PTR [esp],0x8048562
   0x08048449 <+101>:   call   0x804831c <printf@plt>
```
Instead of loading an address, we are simply comparing to `0x149a` which can be decoded directly within gdb
```
(gdb) print 0x149a
$1 = 5274
```
btw, inspecting for strings gives no similar results:
```
IOLI Crackme Level 0x01
Password:
Invalid Password!
Password OK :)
```
I suppose this makes sense. The 0x00 involved loading something into a variable and making a call to `strcmp` where as here we just used the assembly command `cmp`

Can confirm this using a sexier tool provided at [godbolt.org](godbolt.org)

This code
```C
int main(){
    int input;
    scanf("%d",input);
    if (input == 1234)
        printf("ACCESS GRANTED\n");
    else
        printf("ACCESS DENIED\n");
    return 0;
}
```
compiles to this:
```
.LC0:
        .string "%d"
.LC1:
        .string "ACCESS GRANTED"
.LC2:
        .string "ACCESS DENIED"
main:
        push    rbp
        mov     rbp, rsp
        sub     rsp, 16
        mov     eax, DWORD PTR [rbp-4]
        mov     esi, eax
        mov     edi, OFFSET FLAT:.LC0
        mov     eax, 0
        call    __isoc99_scanf
        cmp     DWORD PTR [rbp-4], 1234
        jne     .L2
        mov     edi, OFFSET FLAT:.LC1
        call    puts
        jmp     .L3
.L2:
        mov     edi, OFFSET FLAT:.LC2
        call    puts
.L3:
        mov     eax, 0
        leave
        ret
```
while this code:
```C
#include <stdio.h>
#include <string.h>

int main(){
    char password[] = "password";
    char input[20];
    scanf("%s",input);
    if (strcmp(input,password)==0 )
        printf("ACCESS GRANTED\n");
    else
        printf("ACCESS DENIED\n");
    return 0;
}
```

compiles to this:

```
.LC0:
        .string "%s"
.LC1:
        .string "ACCESS GRANTED"
.LC2:
        .string "ACCESS DENIED"
main:
        push    rbp
        mov     rbp, rsp
        sub     rsp, 32
        movabs  rax, 7237970109966541168
        mov     QWORD PTR [rbp-9], rax
        mov     BYTE PTR [rbp-1], 0
        lea     rax, [rbp-32]
        mov     rsi, rax
        mov     edi, OFFSET FLAT:.LC0
        mov     eax, 0
        call    __isoc99_scanf
        lea     rdx, [rbp-9]
        lea     rax, [rbp-32]
        mov     rsi, rdx
        mov     rdi, rax
        call    strcmp
        test    eax, eax
        jne     .L2
        mov     edi, OFFSET FLAT:.LC1
        call    puts
        jmp     .L3
.L2:
        mov     edi, OFFSET FLAT:.LC2
        call    puts
.L3:
        mov     eax, 0
        leave
        ret
```

##crackme0x02
Following similar steps we can get this disassembled code:
```
   0x08048413 <+47>:    call   0x804831c <printf@plt>
   0x08048418 <+52>:    lea    eax,[ebp-0x4]
   0x0804841b <+55>:    mov    DWORD PTR [esp+0x4],eax
   0x0804841f <+59>:    mov    DWORD PTR [esp],0x804856c
   0x08048426 <+66>:    call   0x804830c <scanf@plt>
=> 0x0804842b <+71>:    mov    DWORD PTR [ebp-0x8],0x5a
   0x08048432 <+78>:    mov    DWORD PTR [ebp-0xc],0x1ec
   0x08048439 <+85>:    mov    edx,DWORD PTR [ebp-0xc]
   0x0804843c <+88>:    lea    eax,[ebp-0x8]
   0x0804843f <+91>:    add    DWORD PTR [eax],edx
   0x08048441 <+93>:    mov    eax,DWORD PTR [ebp-0x8]
   0x08048444 <+96>:    imul   eax,DWORD PTR [ebp-0x8]
   0x08048448 <+100>:   mov    DWORD PTR [ebp-0xc],eax
   0x0804844b <+103>:   mov    eax,DWORD PTR [ebp-0x4]
   0x0804844e <+106>:   cmp    eax,DWORD PTR [ebp-0xc]
   0x08048451 <+109>:   jne    0x8048461 <main+125>
   0x08048453 <+111>:   mov    DWORD PTR [esp],0x804856f
   0x0804845a <+118>:   call   0x804831c <printf@plt>
```

There's a lot of math happening. But I don't think analyzing it does anything because it seems kind of random.  adding edx into the address of eax, moving something from address ebp-0x8 into eax then multiplying by a value in address at ebp-0x4... It's confusing because values are being moved into addresses and then it seems like addresses are being compared to values. In the end there's a cmp with eax and the value stored at address ebp-0xc so I think just examining this value will let us know what to try. We can set a breakpoint here at `0x0804844e <+106>` (because by this point we have performed the instruction at <+103>, saving the value into eax but not doing the cmp which would mess up that value. Examining the value at eax from here gives:
```
(gdb) i r eax
eax            0x52b24             338724
```
So that'll work as a cheap way of getting it and ignoring the assembly. Fortunately it worked.

(NOTE, apparently this value is (90+492)^2, which can probably be ascertained from the stuff happening from <+71> to <+103>, I can see it starting to happen but I am getting confused with all the operations. It seems like values are being pushed to addresses which seems like it would just move the pointers around)
