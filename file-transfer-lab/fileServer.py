#! /usr/bin/env python3
import sys,os
sys.path.append("../lib")       # for params
import re, socket, params
from framedSock import framedReceive, framedSend

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)
title_end = b'title_end'  # to send if end of title
file_name = ""

debug = paramMap['debug']
listenPort = paramMap['listenPort']

if paramMap['usage']:
    params.usage()

l_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)

l_sock.bind(bindAddr)
l_sock.listen(5) # can listen from up 5 sources

print("Waiting for connections (listening) from :", bindAddr)

while True:
    sock, conn_address = l_sock.accept() #waits till connection
    print("Server connected to client from", conn_address) #connection sucssesful
    is_connected = True  # flag for file_interuption
    file_name_flag = True
    
    # forking
    if not os.fork():
    
        while file_name_flag:
            try:
                file_flag = framedReceive(sock, debug)  # get file name
                file_name = file_name + " " + file_flag.decode()
            except:
                print("Nothing recived.")
                file_name = ""
                file_name_flag = False
                sock.close()
                sys.exit(0)
            else:
                if file_flag == title_end:
                    file_name = file_name.replace('title_end','') # removes title_end flag
                    file_name = file_name.replace(' ','')
                    file_name_flag = False

        # Checks to see if the file that is being transfered already exists
        if os.path.isfile( file_name ):
            print("File exists!!!")
            sock.close()
            sys.exit(0)
        else:
            with open(file_name, 'wb') as file:
                print("Writing data.")
                while is_connected:
                    try:
                        t_file_data = framedReceive(sock, debug)  # get the data being sent
                        #print(t_file_data.decode())
                        file.write(t_file_data)
                    except:
                        #print("no more bytes")
                        is_connected = False
                print("File received")
    else:
        sock.close()  # close the socket
