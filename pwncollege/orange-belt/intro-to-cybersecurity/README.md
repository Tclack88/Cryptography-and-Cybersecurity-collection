# Intro To CyberSecurity

## Web Security
`curl --path-as-is`: curl normally squashes input like `../../etc/passwd` This avoids that

Valid command injection operators:

|name|operator|
--------------
| semicolon | ; |
| newline | \n |
| background | & |
| pipe | \| |
| and | && |
| or | \|\| |
| subshell | \`command-string\` |
| subshell | $(command-string) |

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
