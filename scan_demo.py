#!/usr/bin/env python
import socket
target_host = "104.248.191.147"
target_port = 22
# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the client
client.connect((target_host,target_port))
c="GET / HTTP/1.1\r\nHost: 104.248.191.147\r\n\r\n"
byt=c.encode()
# send some data
client.send(byt)
# receive some data
response = client.recv(4096)
print(response.decode())
client.close()

# now do UDP
# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# send some data
c="AAABBBCCC"
byt=c.encode()
client.sendto(byt,(target_host,target_port))
# receive some data
data, addr = client.recvfrom(4096)
print(data)
client.close()

