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

## named pipes
Check out this strange file permission: `prw-r--r--`. That `p` (usually we see it blank `-` for a file, or `d` for a directory, but here it means this file is a named pipe. It can be made with the `mkfifo` command (fifo for first-in-first-out). fifo's will hang until both read and write instructions are received (similar to what happens when you just type `cat`). It's used for complex data flows, when sometimes, input and output commands are received separately.

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

## Permissions and users
permissions can be modified in many ways. Generally it's `chmod OPTIONS FILE`. In typical files we might have: `-rwxrwxrwx`. The first chunk is the owner (called user `u`), the next chunk is the group `g` and the last is everyone else (others `o`). We can also refer to all of these `a`.

* direct assignment: We can imagine these being 1's, so the read flag can be on `100` (bin 4), the write can be on `010` (bin 2) or the execute can be on `001`. We just add those numbers up and it ends up being an octal number (7 is a max) so if we wanted `-rwxr-x-w-` we could do `chmod 752 myfile`

* add or remove: make modifications like `chmod u+w myfile`. It can also be grouped together: `chmod a+r,o+x myfile`

* directly set if we want `-rwxr-x-w-`, we could just do: `chmod u=rwx,g=rx,o=w myfile`. Or if it's blank like `-rwx------`, you can do: `chmod u=rwx,g=-,o=- myfile`

* mix the above two works: `chmod u=rwx,g-w,o+rw`

* suid bit is placed in the location of the `x` of the file owner (`-rwxr-x-w-`), but if there's an `s`, it means that regardless of whoever runs the program (provided it's executable by them), it will run with permissions of the file owner (eg. `-rwsr-x-w-` here, anyone in the group can run the file, but not everyone else). It works by running the suid program, which sets the user id (temporarily) to that of the owner. This gets set by `chmod u+s <progam_name>`

* sticky bit `t` in the "all users" execute portion. Only allows owners of the directory to move/rename (`mv`) files within the directory. A shared directory such as `/tmp` is a common site for this. This can be set with `chmod +t <dir_name>`
```
ls -la /tmp
drwxrwxrwt  7 root root 4096 Aug 11 08:03 ./  <--- sticky bit is the t
```

Looking at the `/etc/passwd`, you will find lines like these:

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
me:x:1000:1000::/home/me:/bin/bash
```

this is `username`,`x`(placeholder for what used to be passwords),`user id`,`group id`,`long form user details`, `home directory`, `default shell`. You can switch users with the `su <user_name>` command. If ran without an argument, it will assume the root user.

Checking out `/etc/shadow` we can see lines like these:

```
root:$6$s74oZg/4.RnUvwo2(quite long))RhjXJ.wjqJ7PprVKLDtg/:19921:0:99999:7:::
daemon:*:19873:0:99999:7:::
mysql:!:19901:0:99999:7::
me:$6$bEFkpM0w/6J0n979$4(quite long)LbAql3ylkVa5ExuPov1.:19921:0:99999:7:::
```
The fields are: `username`,`pw hash`,`date of last pw change`,`min days`, `max days`,`warn`,`inactive`,`expire`. By `max days`, it means how many days since last password change until a new password must be set. `warn` is a countdown until password must be reset, `inactive` is number of days after password expires before the account is disabled. `date of last pw change` is self explanatory and `expire` date of expiration, but note that these are expressed as days since jan 1 1970

The `pw hash` will include, a `$` separated field indicating the hash algorithm used. But sometimes you may see a `*` or a `!` which mean the account is disabled and a blank entry means there is no password

* John the ripper is tailor-made for cracking /etc/shadow files. Simply run `john /etc/shadow` and it will work its magic

## Multiplexing screns
`screen` is a command that will let you work on a terminal without having a new window. After opening, you can press <enter> a few tiems to get to the terminal itself, then to detach you must hit the activation key `<ctrl-A>` followed by `d`. To reattach, just use `screen -r` on that terminal.

## Multiplexing screns
### screen

`screen` is a command that will let you work on a terminal without having a new window. After opening, you can press <enter> a few tiems to get to the terminal itself, then to detach you must hit the activation key `<ctrl-A>` followed by `d`. To reattach, just use `screen -r <session name>` on that terminal. To see all the sessions available, use `screen -ls` then there will be a number.name, kind of like `140.session2` This can be reattached by specifying the name: `screen -r session2`.

### tmux
More modern version of screen. Activation key is `<ctrl-B>` instead. Minor differences in syntax: `tmux ls` and `tmux attach` or `tmux a` for reattaching. `screen` and `tmux` share these activation keys:
* `c` create new window
* `n` next window, `p` previous window
* `0` (or `1`, `2` ... `9` jumps between these 10 allowed windows

Difference in selection menu of each active window:
* screen: `<ctrl-A> "`    Tmux: `<ctrl-B> w` window picker


## extras
* Steps to making a fork bomb: make a shell script which will call itself (twice) in the background (eg. `./myfile.sh &`)

* `cat` is gone, what to do? read! `read MYVAL < file.txt; echo $MYVAL`

* `ls` is gone, what to do? `echo`! `echo` is actually a built-in. `echo *` will list the contents of the currend directory, albeit in a not so pretty way
