# Linux Luminarium 

## Processes
`ps` lists processes, but it's quite boring by itself, you can list "full" content with a `-f` flag, and every process with a `-e` flag

```bash
$ ps
    PID TTY          TIME CMD
  72334 pts/2    00:00:00 bash
  74225 pts/2    00:00:00 ps

$ ps -f
UID          PID    PPID  C STIME TTY          TIME CMD
tclack     72334   72331  0 17:19 pts/2    00:00:00 -bash
tclack     74226   72334  0 19:13 pts/2    00:00:00 ps -f

$ ps -ef
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 Jul13 ?        00:00:49 /sbin/init
root           2       1  0 Jul13 ?        00:00:00 /init
root           6       2  0 Jul13 ?        00:00:00 plan9 --control-socket 7 --log-le
root          67       1  0 Jul13 ?        00:02:33 /lib/systemd/systemd-journald
root          88       1  0 Jul13 ?        00:02:01 /lib/systemd/systemd-udevd
root         100       1  0 Jul13 ?        00:00:00 snapfuse /var/lib/snapd/snaps/bar
(there's much more)
```
The `pts/#`, the number represents which terminal the process is running on (a `?` means there's no terminal interface attached to that process). `TIME` is the total CPU time used up since the process started.

`ps -ef` is standard syntax, but BSD syntax can also be used. To list processes for "all" users (`a`), for it to be	"user-readable" (`u`) and to show all proceses not tieed to a terminal (guessing it's all that "exist"? ) (`x`), then the `aux` (or any subset) can be appended: `ps aux`. The outputs are a little different, such as how `aux` will also show % memory used by CPU, but they're generally quite similar.

```bash
~$ ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0 167412 11968 ?        Ss   Jul13   0:49 /sbin/
root           2  0.0  0.0   3060  1584 ?        Sl   Jul13   0:00 /init
root           6  0.0  0.0   3516  1760 ?        Sl   Jul13   0:00 plan9
root          67  0.0  0.0  72400 13684 ?        S<s  Jul13   2:33 /lib/s
root          88  0.0  0.0  23464  5808 ?        Ss   Jul13   2:02 /lib/s
root         100  0.0  0.0 227756  1408 ?        Ssl  Jul13   0:00 snapfu
(keeps going)
```

Finally, either of the above will truncate information, maybe the whole process won't be shown, you can fix this by adding (to either) some `w`'s (one gives you more, two gives you even more, maybe the full path. It stands for "wide"). 

### terminating, suspending, interrupting...
* `kill` -- Terminate a process by it's id with the kill command (eg. `kill 342`). Note: not `pkill` which terminates based on name or other things.

* `ctrl-c` interrupt a process. If you're stuck in a running process, like a python code running, `ctrl-C` will send an "interrupt" 

* `ctrl-d` end of file (EOF). Good for programs that are constantly reading input from keyboard rather than a file, it's as if the file has ended and it can exit smoothly). 

* `ctrl-z` - SIGTSTP. Suspends the processes (it doesn't terminate, it's just pasued and can be resumed with `fg` or `bg` depending on your preference.

* `fg` -- If a process was suspended from `ctrl-z`, if can be brought back to the "foreground" (to run in the active terminal) with `fg`

* 'bg' -- like fg, but instead of resuming in the terminal, it resumes facelessly in the background

* `&` -- immediately puts a process into the background. instead of running (eg. `./my-program` then typing `ctrl-z` then typing `bg` (three commands in total), you can just move it into the background by adding the `&`: eg. `./my-program &`

Despite the `-f` flag, not all information is being shown, a `-o` flag will allow you to specify the format (o for "output"?) with a comma separated (no spaces) list. You can also specify different options such as stat which will tell the status, such as whether or not a process is sleeping, runnin gin the background, foreground etc.

```bash
$ sleep 100
^Z
[1]+  Stopped                 sleep 100

$ ps -o stat,pid,cmd
STAT     PID CMD
Ss     74505 -bash
T      76070 sleep 100
R+     76071 ps -o stat,pid,cmd
```
a `+` means it's running in the foreground, while any lack of a `+` just means it's in the background. We will see `R`,`S`, or `T`, for Actively `R`unning, `S`leeping, and `T`erminated (suspended, i.e. from the ctrl-z process control). A lower case `s` is also sort of sleeping, really, it's waiting for input. So bash is in the background, not taking up terminal space, you can do other things but also it's waiting for input, thus the `Ss`. To see that sleep command above, we can place it in the background and see a single `S`:
```bash
$ bg
[1]+ sleep 100 &

$ ps -o stat,pid,cmd
STAT     PID CMD
Ss     74505 -bash
S      76104 sleep 100
R+     76106 ps -o stat,pid,cmd
```

