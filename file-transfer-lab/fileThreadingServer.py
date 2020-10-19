#! /usr/bin/env python3
import threading
import time
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
        if lock_file_flag(self.current_file_name):
            lock_thread.acquire()
            write_to_file(self.current_file_name, self.sock)
            lock_thread.release()
        else:
            write_to_file(self.current_file_name, self.sock)

"""
Function used to check if more than one thread is trying to accesse same file. 
@param recives the name of the file

"""        
def lock_file_flag(current_file_name):
    global previous_file_name
    
    print(previous_file_name + " = " + current_file_name)
    if current_file_name == previous_file_name:
        print("Locking file")
        return True
    else:
        previous_file_name = current_file_name 
        print("Running file")
        return False

"""
Function used to infinitly accept socket connedtions and create a thread instance.

"""
def threading_sock():
    while True:
        sock, conn_address = l_sock.accept() #waits till connection
        print("Server connected to client from", conn_address) #connection sucssesful
        server_thread = server(sock)
        server_thread.start()

"""
Function used to handle reciving the name of the file. 
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
            print("Writing data.")
            while is_connected:
                try:
                    t_file_data = framedReceive(sock, debug)  # get the data being sent
                    #print(t_file_data.decode())
                    file.write(t_file_data)
                except:
                    is_connected = False
                    sock.close()
                    sys.exit(0)
                print("File received")

if __name__=="__main__":
    threading_sock()
