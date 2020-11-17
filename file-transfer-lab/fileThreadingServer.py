#! /usr/bin/env python3
import threading
import time
import sys,os
sys.path.append("../lib")       # for params
import re, socket, params
from framedSock import framedReceive, framedSend

file_log = {}

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)
debug = paramMap['debug']
listenPort = paramMap['listenPort']

previous_file_name = "" # int global var for locking file 

if paramMap['usage']:
    params.usage()

l_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)

l_sock.bind(bindAddr)
l_sock.listen(5) # can listen from up 5 sources

print("Waiting for connections (listening) from :", bindAddr)

lock_thread = threading.Lock() # object for locking thread

"""
Class for threading a socket instance.
@param recives a socket

"""
class server(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.current_file_name = ""
    
    def run(self):
        
        self.current_file_name = file_name(self.sock)

        
        if file_log.get(self.current_file_name) == True:
            print("\nSend back to client that file is in being accessed.\n")
            print("\n--------------------------------------------------------------\n")
            example = b'File in use.'
            framedSend(self.sock,example,debug)
        else:
            example = b'File not in use.'
            framedSend(self.sock,example,debug)

            lock_thread.acquire()
            file_log[self.current_file_name] = True
            lock_thread.release()

            write_to_file(self.current_file_name, self.sock)

            #print("\nupdating log")
            lock_thread.acquire()
            file_log[self.current_file_name] = False
            lock_thread.release()
            #print("updated log\n")


"""
Function used to infinitly accept socket connedtions and create a thread instance.

"""
def threading_sock():
    while True:
        sock, conn_address = l_sock.accept() #waits till connection
        print("\nServer connected to client from", conn_address) #connection sucssesful
        server_thread = server(sock)
        server_thread.start()

"""
Function used to handle reciving the name of the file. And communicate with the client
to see if the file being transfer is alerady in use. 
Uses function framed recive from framedSock.
@param recives the instance of the socket connection

"""
def file_name(sock):
    file_name_flag = True
    start_flag = False
    file_name_start = b'title_start' # start of file name flag
    file_name_end = b'title_end'  # end of file name flag
    file_name = ""
    while file_name_flag:
        
        file_flag = framedReceive(sock, debug)  # get file name data
        file_name = file_name + " " + file_flag.decode()

        if start_flag:
            pass
        else:
            if file_flag == file_name_start:
                start_flag = True
                file_name = file_name.replace('title_start','') # removes title_start flag
                file_name = file_name.replace(' ','')
                file_name = file_name.replace('\n','')
            else:
                print("Error: Not name of file")
                sock.close()
                sys.exit(0)
                sock.close()
                
        if file_flag == file_name_end:
            file_name = file_name.replace('title_end','') # removes title_end flag
            file_name = file_name.replace(' ','')
            file_name = file_name.replace('\n','')
            file_name_flag = False
            
    return file_name

"""
Function used for write to file. Uses function framed recive from framedSock.
@param recives the name of file
@param recives the instance of the socket connection
 
"""
def write_to_file(file_name, sock):
    is_connected = True  # flag for file_interuption
    while is_connected:
        with open(file_name, 'wb') as file:
            print("\nWriting data.\n")
            while is_connected:
                try:
                    t_file_data = framedReceive(sock, debug)  # get the data being sent
                    #print(t_file_data.decode())
                    file.write(t_file_data)
                except:
                    is_connected = False
                    sock.close()
            print("File received.")
            print("\n--------------------------------------------------------------\n")
if __name__=="__main__":
    threading_sock()
