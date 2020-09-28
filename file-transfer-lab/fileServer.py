#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    #(('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

#debug = paramMap['debug']
listenPort = paramMap['listenPort']

if paramMap['usage']:
    params.usage()

l_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)

l_sock.bind(bindAddr)
l_sock.listen(5) # can listen from up 5 sources

print("Waiting for connections (listening) from :", bindAddr)

sock, conn_address = l_sock.accept() #waits till connection
print("Server connected to client from", conn_address) #connection sucssesful

with open ("read_file.txt", 'wb') as file:
    print("Reciving Data")
    while True:
        t_file_data = sock.recv(1024)
        print("data: "+data)
        if not data:
            break:
        else:
            file.write(data)
print("File recived")
sock.close()

"""
from framedSock import framedSend, framedReceive

while True:
    payload = framedReceive(sock, debug)
    if debug: print("rec'd: ", payload)
    if not payload:
        break
    payload += b"!"             # make emphatic!
    framedSend(sock, payload, debug)
"""
"""
while 1:
    data = sock.recv(1024).decode()
    if not data: break
    sendMsg = f"Echoing <{data}>"
    print(f"Received <{data}>, sending <{sendMsg}>")
    sendAll(conn_address, sendMsg.encode())
sock.close()#close the socket
"""
