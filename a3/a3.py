import threading
import socket
import os
import re
from time import sleep

serverSocket = socket.socket() 
hostName = socket.gethostname() # returns the name of the local machine
port = 8231
serverIp = (socket.gethostbyname(hostName), port) #a tuple of both the IP address of the host and the port
serverSocket.bind((hostName, port)) #assigns an IP and port to the socket
data = ""

print("This is the server IP: ", serverIp)

#listen for connections
numOfUsers = 64 # change for more users to be supported
serverSocket.listen(numOfUsers) # starts listening for connections
usernames = {'Alex'} # set of usernames

def send(sock, msg): # sends whole message over socket


    string_bytes = (msg + '\n').encode("utf-8", "replace")
    bytes_len = len(string_bytes)
    num_bytes_to_send = bytes_len

    while num_bytes_to_send > 0:
        num_bytes_to_send -= sock.send(string_bytes [bytes_len - num_bytes_to_send:])
        
def recv(sock):
    """Waits until entire message is received from server (until \\n) and returns it"""
    data = sock.recv(4096)
    msg = data.decode("utf-8") # decodes the sent data

    return msg
    
def user_handle(client_sock, client_address):
    while True:
        try: 
            data = serverSocket.recv(client_sock)
            msg = data.split(" ", 1) # splits the received data into command and TXT
            cmd = msg[0], txt = msg[1]
    
            match data:
                case 'LIST\n':
                    usernames = str(usernames)
                    data.send(client_sock, ('List of current users: ' + usernames))
        except:
            print('Error')
              
  

def main():
    while True:
        print('Server has started...\n')
        print('Usernames: ', usernames)
        client_sock, client_address = serverSocket.accept()
        data = recv(client_sock)
        msg = data.split(" ", 1)
        
        if data[1] in usernames:
            client_sock.send('IN-USE\n'.encode('utf-8'))
        else:
            client_sock.send(('HELLO ' + data[1] + '\n').encode('utf-8'))
            usernames.add(data[1])
                 
        server_thread = threading.Thread(target= user_handle, args=(client_sock, client_address))
        server_thread.start()
        
if __name__ == "__main__":
    main()
    







 

