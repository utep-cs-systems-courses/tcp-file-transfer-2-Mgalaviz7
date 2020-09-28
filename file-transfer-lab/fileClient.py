#! /usr/bin/env python3
# Echo client program
import socket, sys, re
 
sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


# Used retrieve input and output files.
input_file = sys.argv[1]
server_file_name = sys.argv[2]

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    #(('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server = paramMap["server"]
usage =  paramMap["usage"]
#debug  = paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)
    
addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)#host IP and Port

s_conn = socket.socket(addrFamily, socktype)

if s_conn is None:
    print('could not open socket')
    sys.exit(1)

s_conn.connect(addrPort)
print("Client connected!")

with open (input_file,'rb') as file:
    t_file_data = file.read(1024)
    while t_file_data:
        s_conn.send(data)
        t_file_data = file.read(1024)
    print("File has been sent")
    s_conn.close()

print("file sennding complete")
"""
print("sending hello world")
framedSend(s_conn, b"hello world", debug)
print("received:", framedReceive(s_conn, debug))

print("sending hello world")
framedSend(s_conn, b"hello world", debug)
print("received:", framedReceive(s, debug))
"""
