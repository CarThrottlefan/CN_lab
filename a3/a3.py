import threading
import socket
import os
import re
from time import sleep

class userData:
    def __init__(self, socket, alias):
        self.sock =  socket
        self.alias = alias

serverSocket = socket.socket() 
hostName = socket.gethostname() # returns the name of the local machine
port = 8231
serverIp = (socket.gethostbyname(hostName), port) #a tuple of both the IP address of the host and the port
serverSocket.bind((hostName, port)) #assigns an IP and port to the socket
data = ""

print("This is the server IP: ", serverIp)

maxUsers = 4 # change for more users to be supported
serverSocket.listen(maxUsers) # starts listening for connections
dummyUser = userData(serverSocket, 'Server')
userSet = {dummyUser} # set of usernames
numOfUsers = 0 # number of connected users


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
    
def user_handle(client_sock, sender_name):
    while True:
        try:  
            userFound = False
            data = recv(client_sock)
            
            if not data: # when a client disconnects
                print(sender_name + ' has closed connection\n')
                for user in userSet:
                    if user.sock == client_sock:
                        
                        userSet.discard(user)
                        global numOfUsers
                        numOfUsers -= 1
                        break
                break

            print('Data from client is ' + data)
            msg = data.split(" ", 2)# splits the received data into command and TXT
            print(msg)
            
            if len(msg) == 1:
                cmd = msg[0]
            elif len(msg) == 3:
                cmd, receiver_name, txt = msg
            else:
                cmd, txt = msg
                receiver_name = ''

            match cmd:
                case 'LIST\n': # handles the list request from the client
                    user_names = {user.alias for user in userSet}
                    users = str(user_names)
                    string = 'List of current users: ' + users
                    send(client_sock, string)
                    
                case cmd if cmd.startswith('SEND'): # handles the message command
                    receiver_name = str(receiver_name)
                    if receiver_name == '': #this is a concession, the empty field is 'Message' - this was done to not make another variable, since 'txt' is what follows 'cmd'
                        send(client_sock, 'BAD-RQST-BODY') # sent when the client doesn't specify a message
                        
                    else:
                        for user in userSet:
                            if user.alias == receiver_name:
                                receiver_sock = user.sock
                                txt = 'DELIVERY ' +  str(sender_name) + ' ' + txt
                                send(client_sock, 'SEND-OK')
                                send(receiver_sock, txt)
                                userFound = True
                            
                    if not userFound:
                        send(client_sock, 'BAD-DEST-USER')
                   
                case cmd:
                    send(client_sock, 'BAD-RQST-HDR') # if the client sends something that is not a command
                
        except OSError as e:
            print("Error: " + e)
            main()

def main():
    while True:
        print('Server has started...\n')
        client_sock, client_address = serverSocket.accept()
        
        data = recv(client_sock)
        msg = data.split(" ", 1) #this contains the list with [command, msg]
        name = msg[1]
        name = name.replace('\n', '') #removes \n from the name to be put in the set
        global maxUsers, numOfUsers 
        
        if(numOfUsers == maxUsers - 1):
            send(client_sock, 'BUSY')
            main()
        
        if any(user.alias == name for user in userSet):
            send(client_sock,"IN-USE")
            main()
            
        else:
            numOfUsers += 1
            print(name + ' has joined\n')
            user_class = userData(client_sock, name)
            userSet.add(user_class)
            
            string = "HELLO " + name
            send(client_sock, string)
                 
        server_thread = threading.Thread(target= user_handle, args=(client_sock, name))
        server_thread.start()
        
if __name__ == "__main__":
    
    main()
    
