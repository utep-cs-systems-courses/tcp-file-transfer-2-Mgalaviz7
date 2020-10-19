#! /usr/bin/env python3

import socket, sys, re, os 
sys.path.append("../lib")       # for params
import params
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
    (('-f', '--file'), "file", " "),  # used to get input file
    (('-o', '--outfile'), "outfile", " "),  # used to get server file name
    )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server = paramMap["server"]
debug = paramMap["debug"]
usage = paramMap["usage"]
input_file = paramMap["file"]
server_file_name = paramMap["outfile"]

if usage:
    params.usage()

def socket_connection(server):    
    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)
    
    addrFamily = socket.AF_INET
    socktype = socket.SOCK_STREAM
    addrPort = (serverHost, serverPort)  # host IP and Port

    s_conn = socket.socket(addrFamily, socktype)

    if s_conn is None:
        print('could not open socket')
        sys.exit(1)

    s_conn.connect(addrPort)
    print("Client connected!")
    send_file(s_conn)


def file_handler(input_file, server):
    # checks on client side if file exists
    if not os.path.isfile(input_file):
        print("File does not exists!!!")
        sys.exit(0)
    # check to see if file is empty
    if os.path.getsize(input_file) == 0:
        print(input_file + " is empty")
        sys.exit(0)
    else:
        socket_connection(server)

"""
Function used to handle reciving the name of the file. 
Uses function framed recive from framedSock.
@param recives the instance of the socket connection

"""
def send_file(s_conn):    
    
    file_name_start = b'title_start' # start of file name flag
    file_name_end = b'title_end'  # end of file name flag
    framedSend(s_conn, file_name_start, debug)
    # send the name of how the file will be save on the server
    framedSend(s_conn, server_file_name.encode(), debug)
    framedSend(s_conn, file_name_end, debug)

    with open(input_file, 'rb') as file:
        t_file_data = file.read(100)  # only 100 bytes becasue of framedSock
        if not t_file_data:
            print("Finished sending bytes")
        else:
            while t_file_data:
                framedSend(s_conn, t_file_data, debug)
                t_file_data = file.read(100)  # only 100 bytes becasue of framedSock
    print("File has been sent")
    s_conn.close()                

if __name__=="__main__":
    file_handler(input_file, server)
