# CTFCafe (Reverse engineering challenge)

## contents
	* Dockerfile -- my glibc couldn't update enough to run this, so this is just a build file so I could run in a container
	* ctf_cafe -- the binary

## 
Run the binary:

===== 🍔 Welcome to the CTF Cafe! =====
1. View Menu
2. Place Order
3. View Total
0. Exit

This is like a lame text game where you can order hamburgers and stuff. Decompiling the (relevant) portion of main we can see a scanf (takiing in our choice 1-4) as well as several compare and nump if equal. These are clearly the 4 choices of the game. But we can see at `main <+123>` there's a compare to the number 9 which is clearly not the four listed. In this case it jumps and prints something.

```
   0x00000000004004e5 <+63>:    mov    $0x0,%eax
   0x00000000004004ea <+68>:    call   0x400390 <printf@plt>
   0x00000000004004ef <+73>:    lea    -0x8(%rbp),%rax
   0x00000000004004f3 <+77>:    mov    %rax,%rsi
   0x00000000004004f6 <+80>:    mov    $0x401371,%edi
   0x00000000004004fb <+85>:    mov    $0x0,%eax
   0x0000000000400500 <+90>:    call   0x4003a0 <__isoc23_scanf@plt>
   0x0000000000400505 <+95>:    cmp    $0x1,%eax
   0x0000000000400508 <+98>:    je     0x40051e <main+120>
   0x000000000040050a <+100>:   call   0x4007a9 <clear_input>
   0x000000000040050f <+105>:   mov    $0x401378,%edi
   0x0000000000400514 <+110>:   call   0x400380 <puts@plt>
   0x0000000000400519 <+115>:   jmp    0x400669 <main+451>
   0x000000000040051e <+120>:   mov    -0x8(%rbp),%eax
   0x0000000000400521 <+123>:   cmp    $0x9,%eax
   0x0000000000400524 <+126>:   je     0x40058a <main+228>
   0x0000000000400526 <+128>:   cmp    $0x9,%eax
   0x0000000000400529 <+131>:   jg     0x40065f <main+441>
   0x000000000040052f <+137>:   cmp    $0x3,%eax
   0x0000000000400532 <+140>:   je     0x40056c <main+198>
   0x0000000000400534 <+142>:   cmp    $0x3,%eax
   0x0000000000400537 <+145>:   jg     0x40065f <main+441>
   0x000000000040053d <+151>:   cmp    $0x2,%eax
   0x0000000000400540 <+154>:   je     0x400562 <main+188>
   0x0000000000400542 <+156>:   cmp    $0x2,%eax
   0x0000000000400545 <+159>:   jg     0x40065f <main+441>
   0x000000000040054b <+165>:   test   %eax,%eax
   0x000000000040054d <+167>:   je     0x400576 <main+208>
   0x000000000040054f <+169>:   cmp    $0x1,%eax
   0x0000000000400552 <+172>:   jne    0x40065f <main+441>
   0x0000000000400558 <+178>:   call   0x400670 <print_menu>
   0x000000000040055d <+183>:   jmp    0x400669 <main+451>
   0x0000000000400562 <+188>:   call   0x4006b0 <place_order>
   0x0000000000400567 <+193>:   jmp    0x400669 <main+451>
   0x000000000040056c <+198>:   call   0x400779 <view_total>
   0x0000000000400571 <+203>:   jmp    0x400669 <main+451>
   0x0000000000400576 <+208>:   mov    $0x40139e,%edi
   0x000000000040057b <+213>:   call   0x400380 <puts@plt>
   0x0000000000400580 <+218>:   mov    $0x0,%eax
   0x0000000000400585 <+223>:   jmp    0x40066e <main+456>
   0x000000000040058a <+228>:   mov    $0x4013c0,%edi
   0x000000000040058f <+233>:   call   0x400380 <puts@plt>
   0x0000000000400594 <+238>:   mov    $0x401410,%edi
   0x0000000000400599 <+243>:   mov    $0x0,%eax
   0x000000000040059e <+248>:   call   0x400390 <printf@plt>
   0x00000000004005a3 <+253>:   mov    $0x4030f8,%esi
   0x00000000004005a8 <+258>:   mov    $0x401442,%edi
   0x00000000004005ad <+263>:   mov    $0x0,%eax
   0x00000000004005b2 <+268>:   call   0x4003a0 <__isoc23_scanf@plt>
   0x00000000004005b7 <+273>:   cmp    $0x1,%eax
   0x00000000004005ba <+276>:   je     0x4005d0 <main+298>
   0x00000000004005bc <+278>:   mov    $0x401446,%edi
   0x00000000004005c1 <+283>:   call   0x400380 <puts@plt>
   0x00000000004005c6 <+288>:   mov    $0x1,%eax
   0x00000000004005cb <+293>:   jmp    0x40066e <main+456>
   0x00000000004005d0 <+298>:   mov    0x2b21(%rip),%rdx        # 0x4030f8 <key>
   0x00000000004005d7 <+305>:   movabs $0x9bd2c75a49c4efeb,%rax
   0x00000000004005e1 <+315>:   cmp    %rax,%rdx
   0x00000000004005e4 <+318>:   je     0x4005f2 <main+332>
   0x00000000004005e6 <+320>:   mov    $0x401458,%edi
   0x00000000004005eb <+325>:   call   0x400380 <puts@plt>
   0x00000000004005f0 <+330>:   jmp    0x40065f <main+441>
   0x00000000004005f2 <+332>:   mov    $0x401490,%edi
   0x00000000004005f7 <+337>:   call   0x400380 <puts@plt>
   0x00000000004005fc <+342>:   mov    $0x4014cc,%edi
   0x0000000000400601 <+347>:   mov    $0x0,%eax
   0x0000000000400606 <+352>:   call   0x400390 <printf@plt>
   0x000000000040060b <+357>:   movl   $0x0,-0x4(%rbp)
```

Testing this choice 9

```
Oh, so you want the secret sauce recipe? Only if you have our proprietary key!
Enter 8-byte hex key (e.g., 0x0123456789ABCDEF):
```

Opening this back up with gdb, we can see a call to load some hex value and print
Following the chain all the way down at `main <+305>` A large hex value stands out (it's larger than any memory address for sure) is moved into `rax`, then it's compared with `rdx` (our input value). We can try this hex value: `0x9bd2c75a49c4efeb`

```
===== 🍔 Welcome to the CTF Cafe! =====
1. View Menu
2. Place Order
3. View Total
0. Exit
Enter your choice: 9
Oh, so you want the secret sauce recipe? Only if you have our proprietary key!
Enter 8-byte hex key (e.g., 0x0123456789ABCDEF): 0x9bd2c75a49c4efeb
Congratulations! You have unlocked the secret sauce recipe!
Secret Sauce: SVBGR{d3c0mp1l3rs_m4k3_l1f3_34sy}
Invalid choice. Try again.
```

flag found: SVBGR{d3c0mp1l3rs_m4k3_l1f3_34sy}

