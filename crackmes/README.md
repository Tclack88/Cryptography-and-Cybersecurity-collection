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
EDIT: actually I can see it now. operations like `mov    DWORD PTR [ebp-0xc],0x1ec` are moving for example 492 into the address that points to ebp-0xc, storing it there. With some careful following, it's ascertainable.

##crackme0x03
Without just looking ahead I want to try to figure out the assembly. 

```
0x080484b4 <+28>:    mov    DWORD PTR [esp],0x8048610
   0x080484bb <+35>:    call   0x8048350 <printf@plt>
   0x080484c0 <+40>:    mov    DWORD PTR [esp],0x8048629
   0x080484c7 <+47>:    call   0x8048350 <printf@plt>
   0x080484cc <+52>:    lea    eax,[ebp-0x4]
   0x080484cf <+55>:    mov    DWORD PTR [esp+0x4],eax
   0x080484d3 <+59>:    mov    DWORD PTR [esp],0x8048634
   0x080484da <+66>:    call   0x8048330 <scanf@plt>
   0x080484df <+71>:    mov    DWORD PTR [ebp-0x8],0x5a
   0x080484e6 <+78>:    mov    DWORD PTR [ebp-0xc],0x1ec
   0x080484ed <+85>:    mov    edx,DWORD PTR [ebp-0xc]
   0x080484f0 <+88>:    lea    eax,[ebp-0x8]
   0x080484f3 <+91>:    add    DWORD PTR [eax],edx
   0x080484f5 <+93>:    mov    eax,DWORD PTR [ebp-0x8]
   0x080484f8 <+96>:    imul   eax,DWORD PTR [ebp-0x8]
   0x080484fc <+100>:   mov    DWORD PTR [ebp-0xc],eax
   0x080484ff <+103>:   mov    eax,DWORD PTR [ebp-0xc]
   0x08048502 <+106>:   mov    DWORD PTR [esp+0x4],eax
   0x08048506 <+110>:   mov    eax,DWORD PTR [ebp-0x4]
   0x08048509 <+113>:   mov    DWORD PTR [esp],eax
   0x0804850c <+116>:   call   0x804846e <test>
   0x08048511 <+121>:   mov    eax,0x0
   0x08048516 <+126>:   leave
   0x08048517 <+127>:   ret
```
Clearly input is being taken in and stored into esp+0x4 (I think?) at`<+55>`, it's not being referenced again until `<+106>` when the intermediate operations are being performed. We can see 90 and 492 both being brought in as before. They're being added again (after some intermediate loading) at `<+91>` and storing 582 at ebp+0x8. It's being squared again (338724 as before) then that's being stored at ebp-0xc. Okay so then it's doing a call of a function called test

```
0804846e <test>:
 804846e:       55                      push   ebp
 804846f:       89 e5                   mov    ebp,esp
 8048471:       83 ec 08                sub    esp,0x8
 8048474:       8b 45 08                mov    eax,DWORD PTR [ebp+0x8]
 8048477:       3b 45 0c                cmp    eax,DWORD PTR [ebp+0xc]
 804847a:       74 0e                   je     804848a <test+0x1c>
 804847c:       c7 04 24 ec 85 04 08    mov    DWORD PTR [esp],0x80485ec
 8048483:       e8 8c ff ff ff          call   8048414 <shift>
 8048488:       eb 0c                   jmp    8048496 <test+0x28>
 804848a:       c7 04 24 fe 85 04 08    mov    DWORD PTR [esp],0x80485fe
 8048491:       e8 7e ff ff ff          call   8048414 <shift>
 8048496:       c9                      leave
 8048497:       c3                      ret
```
This just does the same. So a bit of a waste for me to analyze as we are just exporting the cmp to this test. Same password though, 338724. Hopefully the next one.

##crackme0x04
checking out (a portion of) main directly
```
   0x0804853b <+50>:    call   0x8048394 <printf@plt>
   0x08048540 <+55>:    lea    eax,[ebp-0x78]
   0x08048543 <+58>:    mov    DWORD PTR [esp+0x4],eax
   0x08048547 <+62>:    mov    DWORD PTR [esp],0x8048682
   0x0804854e <+69>:    call   0x8048374 <scanf@plt>
   0x08048553 <+74>:    lea    eax,[ebp-0x78]
   0x08048556 <+77>:    mov    DWORD PTR [esp],eax
   0x08048559 <+80>:    call   0x8048484 <check>
   0x0804855e <+85>:    mov    eax,0x0
   0x08048563 <+90>:    leave
   0x08048564 <+91>:    ret
```
We are scanning in the input to ebp-0x78 then we are calling the check function:
```
0x08048484 <+0>:     push   ebp
   0x08048485 <+1>:     mov    ebp,esp
   0x08048487 <+3>:     sub    esp,0x28
   0x0804848a <+6>:     mov    DWORD PTR [ebp-0x8],0x0
   0x08048491 <+13>:    mov    DWORD PTR [ebp-0xc],0x0
   0x08048498 <+20>:    mov    eax,DWORD PTR [ebp+0x8]
   0x0804849b <+23>:    mov    DWORD PTR [esp],eax
   0x0804849e <+26>:    call   0x8048384 <strlen@plt>
   0x080484a3 <+31>:    cmp    DWORD PTR [ebp-0xc],eax
   0x080484a6 <+34>:    jae    0x80484fb <check+119>
   0x080484a8 <+36>:    mov    eax,DWORD PTR [ebp-0xc]
   0x080484ab <+39>:    add    eax,DWORD PTR [ebp+0x8]
   0x080484ae <+42>:    movzx  eax,BYTE PTR [eax]
   0x080484b1 <+45>:    mov    BYTE PTR [ebp-0xd],al
   0x080484b4 <+48>:    lea    eax,[ebp-0x4]
   0x080484b7 <+51>:    mov    DWORD PTR [esp+0x8],eax
   0x080484bb <+55>:    mov    DWORD PTR [esp+0x4],0x8048638
   0x080484c3 <+63>:    lea    eax,[ebp-0xd]
   0x080484c6 <+66>:    mov    DWORD PTR [esp],eax
   0x080484c9 <+69>:    call   0x80483a4 <sscanf@plt>
   0x080484ce <+74>:    mov    edx,DWORD PTR [ebp-0x4]
   0x080484d1 <+77>:    lea    eax,[ebp-0x8]
   0x080484d4 <+80>:    add    DWORD PTR [eax],edx
   0x080484d6 <+82>:    cmp    DWORD PTR [ebp-0x8],0xf
   0x080484da <+86>:    jne    0x80484f4 <check+112>
   0x080484dc <+88>:    mov    DWORD PTR [esp],0x804863b
   0x080484e3 <+95>:    call   0x8048394 <printf@plt>
   0x080484e8 <+100>:   mov    DWORD PTR [esp],0x0
   0x080484ef <+107>:   call   0x80483b4 <exit@plt>
   0x080484f4 <+112>:   lea    eax,[ebp-0xc]
   0x080484f7 <+115>:   inc    DWORD PTR [eax]
   0x080484f9 <+117>:   jmp    0x8048498 <check+20>
   0x080484fb <+119>:   mov    DWORD PTR [esp],0x8048649
   0x08048502 <+126>:   call   0x8048394 <printf@plt>
   0x08048507 <+131>:   leave
   0x08048508 <+132>:   ret
```

We are loading 0 into eax then calling string length. I am guessing this is checking that we don't supply an empty string. Afterward is a jae (like jge but for unsigned integers), it jumps straight to `<+119>` which loads and prints "incorrect password", nothing special like "password too short". I actually was looking ahead at `<+82>` and guessed it was checking if the length of the password was 15, so I put in 15 1's and it was correct. However repeating with 15 2's doesn't. Experiementing some more I found that as long as the sum of digits is 15, then it works. so 22222221 works, or 771, or 96, etc. So I accidentally got this one also. I guess the  length is setting a limit to check, we can see an increment and then jump back to the beginning at `<+115>` and `<+117>`. I guess maybe the movzx is what is checking our single digit. It moves something and then zero fills it, so probably getting each digit. Oh well.

##crackme0x05
So this one is like the same. Main scans in user input then calls a `check` function. Which is very much the same:

```
Dump of assembler code for function check:
   0x080484c8 <+0>:     push   ebp
   0x080484c9 <+1>:     mov    ebp,esp
   0x080484cb <+3>:     sub    esp,0x28
   0x080484ce <+6>:     mov    DWORD PTR [ebp-0x8],0x0
   0x080484d5 <+13>:    mov    DWORD PTR [ebp-0xc],0x0
   0x080484dc <+20>:    mov    eax,DWORD PTR [ebp+0x8]
   0x080484df <+23>:    mov    DWORD PTR [esp],eax
   0x080484e2 <+26>:    call   0x8048384 <strlen@plt>
   0x080484e7 <+31>:    cmp    DWORD PTR [ebp-0xc],eax
   0x080484ea <+34>:    jae    0x8048532 <check+106>
   0x080484ec <+36>:    mov    eax,DWORD PTR [ebp-0xc]
   0x080484ef <+39>:    add    eax,DWORD PTR [ebp+0x8]
   0x080484f2 <+42>:    movzx  eax,BYTE PTR [eax]
   0x080484f5 <+45>:    mov    BYTE PTR [ebp-0xd],al
   0x080484f8 <+48>:    lea    eax,[ebp-0x4]
   0x080484fb <+51>:    mov    DWORD PTR [esp+0x8],eax
   0x080484ff <+55>:    mov    DWORD PTR [esp+0x4],0x8048668
   0x08048507 <+63>:    lea    eax,[ebp-0xd]
   0x0804850a <+66>:    mov    DWORD PTR [esp],eax
   0x0804850d <+69>:    call   0x80483a4 <sscanf@plt>
   0x08048512 <+74>:    mov    edx,DWORD PTR [ebp-0x4]
   0x08048515 <+77>:    lea    eax,[ebp-0x8]
   0x08048518 <+80>:    add    DWORD PTR [eax],edx
   0x0804851a <+82>:    cmp    DWORD PTR [ebp-0x8],0x10
   0x0804851e <+86>:    jne    0x804852b <check+99>
   0x08048520 <+88>:    mov    eax,DWORD PTR [ebp+0x8]
   0x08048523 <+91>:    mov    DWORD PTR [esp],eax
   0x08048526 <+94>:    call   0x8048484 <parell>
   0x0804852b <+99>:    lea    eax,[ebp-0xc]
   0x0804852e <+102>:   inc    DWORD PTR [eax]
   0x08048530 <+104>:   jmp    0x80484dc <check+20>
   0x08048532 <+106>:   mov    DWORD PTR [esp],0x8048679
   0x08048539 <+113>:   call   0x8048394 <printf@plt>
   0x0804853e <+118>:   leave
   0x0804853f <+119>:   ret
```
but we can see at `<+82>` the value is checked against 0x10 (or integer 16). So trying a pasword like 88 does the trick. Hopefeully I can understand the assembly at some point.

##crackme0x07
TODO

