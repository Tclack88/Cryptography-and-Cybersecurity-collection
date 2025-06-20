
$ ./donut
Welcome to the donut shop!
Please enter your timezone so that we can tailor your experience for today:
> 0
Timezone set to 0!
Options:
1. Buy a donut
2. Earn money to use in the shop
3. Maintenance
4. Exit

Buying a donut costs $50 (you begin with $1330). Earn money to use in the shop seems like a guessing game. You can attempt to earn money by guessing a number. It appears that incorrect guesses cuts your remaining amount in half, it does not go negative)

Changing the time zone seems arbitrary, It doesn't seem to give you different amounts of starting money or open the maintenance option. This maintenance option seems enticing. And a quick check of strings on the program leads me to believe this is the admin panel:

$ strings donut
.
.
.
You have %d dollars
How many donuts would you like to buy?
Invalid amount of donuts!
Not enough money!
Bought %d donuts. Your balance is now %d.
What is your guess?
Correct! You get $50
Oops, you lost half of your money!
You aren't authorized to access this! <---- this is given when 3 is selected
Welcome to the admin panel!          <-------- this is shown right after
Date:
date --date='TZ="%s"'
What would you like to set your balance to?
Balance set!
Options:
1. Buy a donut
2. Earn money to use in the shop
3. Maintenance
4. Exit
Welcome to the donut shop!
Please enter your timezone so that we can tailor your experience for today:
Timezone set to %s!
Unknown choice!
9*3$"
America/Los_Angeles
.
.
.

Looking into the compiled code we can see that selecting certain choices will call the associated function. We can see that in line 1687 that if 3 is selected, maintenance function is called


    165f:       83 f8 01                cmp    eax,0x1
    1662:       75 0c                   jne    1670 <main+0xd6>
    1664:       b8 00 00 00 00          mov    eax,0x0
    1669:       e8 db fb ff ff          call   1249 <buy>
    166e:       eb b3                   jmp    1623 <main+0x89>
    1670:       8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
    1673:       83 f8 02                cmp    eax,0x2
    1676:       75 0c                   jne    1684 <main+0xea>
    1678:       b8 00 00 00 00          mov    eax,0x0
    167d:       e8 d4 fc ff ff          call   1356 <earn>
    1682:       eb 9f                   jmp    1623 <main+0x89>
    1684:       8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
    1687:       83 f8 03                cmp    eax,0x3
    168a:       75 0c                   jne    1698 <main+0xfe>
    168c:       b8 00 00 00 00          mov    eax,0x0
    1691:       e8 94 fd ff ff          call   142a <maintenance>



000000000000142a <maintenance>:
    142a:       f3 0f 1e fa             endbr64
    142e:       55                      push   rbp
    142f:       48 89 e5                mov    rbp,rsp
    1432:       48 83 ec 70             sub    rsp,0x70
    1436:       64 48 8b 04 25 28 00    mov    rax,QWORD PTR fs:0x28
    143d:       00 00
    143f:       48 89 45 f8             mov    QWORD PTR [rbp-0x8],rax
    1443:       31 c0                   xor    eax,eax
    1445:       8b 05 f9 2b 00 00       mov    eax,DWORD PTR [rip+0x2bf9]        # 4044 <donuts>
    144b:       3d be ba fe ca          cmp    eax,0xcafebabe         <------ something is being compared to 0xcafebabe
    1450:       74 14                   je     1466 <maintenance+0x3c>
    1452:       48 8d 05 a7 0c 00 00    lea    rax,[rip+0xca7]        # 2100 <_IO_stdin_used+0x100>
    1459:       48 89 c7                mov    rdi,rax
    145c:       e8 6f fc ff ff          call   10d0 <_init+0xd0>
    1461:       e9 a1 00 00 00          jmp    1507 <maintenance+0xdd>
    1466:       48 8d 05 b9 0c 00 00    lea    rax,[rip+0xcb9]        # 2126 <_IO_stdin_used+0x126>
    146d:       48 89 c7                mov    rdi,rax
    1470:       e8 5b fc ff ff          call   10d0 <_init+0xd0>
    1475:       48 8d 05 c6 0c 00 00    lea    rax,[rip+0xcc6]        # 2142 <_IO_stdin_used+0x142>
    147c:       48 89 c7                mov    rdi,rax
    147f:       e8 4c fc ff ff          call   10d0 <_init+0xd0>
    1484:       48 8d 45 90             lea    rax,[rbp-0x70]
    1488:       48 8d 15 91 2b 00 00    lea    rdx,[rip+0x2b91]        # 4020 <timezone>
    148f:       48 89 d1                mov    rcx,rdx
    1492:       48 8d 15 af 0c 00 00    lea    rdx,[rip+0xcaf]        # 2148 <_IO_stdin_used+0x148>
    1499:       be 64 00 00 00          mov    esi,0x64
    149e:       48 89 c7                mov    rdi,rax
    14a1:       b8 00 00 00 00          mov    eax,0x0
    14a6:       e8 65 fc ff ff          call   1110 <_init+0x110>
    14ab:       48 8d 45 90             lea    rax,[rbp-0x70]
    14af:       48 89 c7                mov    rdi,rax
    14b2:       e8 39 fc ff ff          call   10f0 <_init+0xf0>
    14b7:       48 8d 05 a2 0c 00 00    lea    rax,[rip+0xca2]        # 2160 <_IO_stdin_used+0x160>
    14be:       48 89 c7                mov    rdi,rax
    14c1:       e8 0a fc ff ff          call   10d0 <_init+0xd0>
    14c6:       48 8d 05 7a 0b 00 00    lea    rax,[rip+0xb7a]        # 2047 <_IO_stdin_used+0x47>
    14cd:       48 89 c7                mov    rdi,rax
    14d0:       b8 00 00 00 00          mov    eax,0x0
    14d5:       e8 26 fc ff ff          call   1100 <_init+0x100>
    14da:       48 8d 05 5f 2b 00 00    lea    rax,[rip+0x2b5f]        # 4040 <money>
    14e1:       48 89 c6                mov    rsi,rax
    14e4:       48 8d 05 5f 0b 00 00    lea    rax,[rip+0xb5f]        # 204a <_IO_stdin_used+0x4a>
    14eb:       48 89 c7                mov    rdi,rax
    14ee:       b8 00 00 00 00          mov    eax,0x0
    14f3:       e8 48 fc ff ff          call   1140 <_init+0x140>
    14f8:       48 8d 05 8d 0c 00 00    lea    rax,[rip+0xc8d]        # 218c <_IO_stdin_used+0x18c>
    14ff:       48 89 c7                mov    rdi,rax
    1502:       e8 c9 fb ff ff          call   10d0 <_init+0xd0>
    1507:       48 8b 45 f8             mov    rax,QWORD PTR [rbp-0x8]
    150b:       64 48 2b 04 25 28 00    sub    rax,QWORD PTR fs:0x28
    1512:       00 00
    1514:       74 05                   je     151b <maintenance+0xf1>
    1516:       e8 c5 fb ff ff          call   10e0 <_init+0xe0>
    151b:       c9                      leave
    151c:       c3                      ret

Something is being compared to 0xcafebabe, by the looks of it probably the number of donuts. But that's 3405691582 donuts? We can't buy that many. Perhaps we can Earn money and buy a certain amount to get it. But we need to get that number. The guess could be hardcoded, so let's look into the assembly for it:

(gdb) disas earn

0000000000001356 <earn>:
    1356:       f3 0f 1e fa             endbr64
    135a:       55                      push   rbp
    135b:       48 89 e5                mov    rbp,rsp
    135e:       48 83 ec 10             sub    rsp,0x10
    1362:       64 48 8b 04 25 28 00    mov    rax,QWORD PTR fs:0x28
    1369:       00 00
    136b:       48 89 45 f8             mov    QWORD PTR [rbp-0x8],rax
    136f:       31 c0                   xor    eax,eax
    1371:       48 8d 45 f0             lea    rax,[rbp-0x10]
    1375:       ba 00 00 00 00          mov    edx,0x0
    137a:       be 04 00 00 00          mov    esi,0x4
    137f:       48 89 c7                mov    rdi,rax
    1382:       e8 c9 fd ff ff          call   1150 <_init+0x150>
    1387:       48 8d 05 1d 0d 00 00    lea    rax,[rip+0xd1d]        # 20ab <_IO_stdin_used+0xab>
    138e:       48 89 c7                mov    rdi,rax
    1391:       e8 3a fd ff ff          call   10d0 <_init+0xd0>
    1396:       48 8d 05 aa 0c 00 00    lea    rax,[rip+0xcaa]        # 2047 <_IO_stdin_used+0x47>
    139d:       48 89 c7                mov    rdi,rax
    13a0:       b8 00 00 00 00          mov    eax,0x0
    13a5:       e8 56 fd ff ff          call   1100 <_init+0x100>
    13aa:       48 8d 45 f4             lea    rax,[rbp-0xc]
    13ae:       48 89 c6                mov    rsi,rax
    13b1:       48 8d 05 92 0c 00 00    lea    rax,[rip+0xc92]        # 204a <_IO_stdin_used+0x4a>
    13b8:       48 89 c7                mov    rdi,rax
    13bb:       b8 00 00 00 00          mov    eax,0x0
    13c0:       e8 7b fd ff ff          call   1140 <_init+0x140>
    13c5:       8b 55 f4                mov    edx,DWORD PTR [rbp-0xc]
    13c8:       8b 45 f0                mov    eax,DWORD PTR [rbp-0x10]
    13cb:       39 c2                   cmp    edx,eax
    13cd:       75 20                   jne    13ef <earn+0x99>
    13cf:       48 8d 05 e9 0c 00 00    lea    rax,[rip+0xce9]        # 20bf <_IO_stdin_used+0xbf>
    13d6:       48 89 c7                mov    rdi,rax
    13d9:       e8 f2 fc ff ff          call   10d0 <_init+0xd0>
    13de:       8b 05 5c 2c 00 00       mov    eax,DWORD PTR [rip+0x2c5c]        # 4040 <money>
    13e4:       83 c0 32                add    eax,0x32
    13e7:       89 05 53 2c 00 00       mov    DWORD PTR [rip+0x2c53],eax        # 4040 <money>
    13ed:       eb 24                   jmp    1413 <earn+0xbd>
    13ef:       48 8d 05 e2 0c 00 00    lea    rax,[rip+0xce2]        # 20d8 <_IO_stdin_used+0xd8>
    13f6:       48 89 c7                mov    rdi,rax
    13f9:       e8 d2 fc ff ff          call   10d0 <_init+0xd0>
    13fe:       8b 05 3c 2c 00 00       mov    eax,DWORD PTR [rip+0x2c3c]        # 4040 <money>
    1404:       89 c2                   mov    edx,eax
    1406:       c1 ea 1f                shr    edx,0x1f
    1409:       01 d0                   add    eax,edx
    140b:       d1 f8                   sar    eax,1
    140d:       89 05 2d 2c 00 00       mov    DWORD PTR [rip+0x2c2d],eax        # 4040 <money>
    1413:       90                      nop
    1414:       48 8b 45 f8             mov    rax,QWORD PTR [rbp-0x8]
    1418:       64 48 2b 04 25 28 00    sub    rax,QWORD PTR fs:0x28
    141f:       00 00
    1421:       74 05                   je     1428 <earn+0xd2>
    1423:       e8 b8 fc ff ff          call   10e0 <_init+0xe0>
    1428:       c9                      leave
    1429:       c3                      ret

In particular we have these lines where we are comparing the value ar rbp-0xc with rbp-0x10:

13c5:       8b 55 f4                mov    edx,DWORD PTR [rbp-0xc]
13c8:       8b 45 f0                mov    eax,DWORD PTR [rbp-0x10]


in GDB
0x7fffffffe054: 0x02    0x00    0x00    0x00
(gdb) x/4x ($rbp-0xc)
0x7fffffffe054: 0x02    0x00    0x00    0x00
(gdb) x/4x ($rbp-0x10)
0x7fffffffe050: 0x8a    0xb1    0xe2    0x2f
(gdb) ni
(gdb) c
Continuing.

>>> int(0x2fe2b18a)
803385738

803385738
Correct! You get $50


wow, a whole $50. This will be slow (assuming the value doesn't change each time). Checking it another round:


(gdb) x/4x ($rbp-0x10)
0x7fffffffe050: 0x26    0x5a    0x10    0x03
(gdb) ni
51403302

>>> int(0x03105a26)
51403302

Correct! You get $50

Yes, it does indeed. We're going to have to figure out where this number comes from


This timezone thing is also a bit mysterious. I can check the value here:
1488:       48 8d 15 91 2b 00 00    lea    rdx,[rip+0x2b91]        # 4020 <timezone>

It says "America/Los_Angeles"
