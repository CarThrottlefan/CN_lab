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

numOfUsers = 64 # change for more users to be supported
serverSocket.listen(numOfUsers) # starts listening for connections
nullUser = userData(serverSocket, 'Server')
userSet = {nullUser} # set of usernames
userNames = {'Alex'}
#user_info = [] #list of user sockets+names, each user a tuple

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
            #if input == '!quit': #FIXME implement a quit/shutdown function for the server
                #os._exit(1)
            
            data = recv(client_sock)
            print('Data from client is ' + data)
            msg = data.split(" ", 1)# splits the received data into command and TXT
            msg_set = set(msg)
            
            if len(msg) == 1:
                cmd = msg[0]
            elif len(msg) == 3:
                cmd = msg[0]
                username = msg[1]
                txt = msg[2]  
            else:
                cmd = msg[0], txt = msg[1]

            match cmd:
                case 'LIST\n':
                    print('It gets here')
                    user_names = {user.alias for user in userSet}
                    users = str(user_names)
                    print('It gets here 2')
                    #users = str(usernames) #converts the set of users to a string
                    print(users)
                    string = 'List of current users: ' + users
                    send(client_sock, string)
                    
                #case cmd if cmd.startswith('SEND'):
                    #FIXME seatch for the username in the list of tuples, then access said tuple and get the socket
                    
                case cmd:
                    continue
                
        except:
            print('Error 1')
            os._exit(1)

def main():
    while True:
        print('Server has started...\n')
        #print('Usernames: ', usernamesSet)
        print(type(userSet))
        client_sock, client_address = serverSocket.accept()
        
        data = recv(client_sock)
        msg = data.split(" ", 1) #this contains the list with [command, msg]
        name = msg[1]
        name = name.replace('\n', '') #removes \n from the name to be put in the set
        
        global numOfUsers #FIXME implement a way to check if max num of connections is not reached
        
        if name in userNames:
            send(client_sock,"IN-USE")
            main()
        else:
            user_class = userData(client_sock, name)
            userSet.add(user_class)
            #user_tuple = (client_sock, name) #generates a tuple of a user's name+socket
            #print(usernamesSet)
            #user_info.append(user_tuple) #appends each new user's tuple to a list of connected user's tuples
            #print(user_info)
            string = "HELLO " + name
            send(client_sock, string)
            userNames.add(name)
                 
        server_thread = threading.Thread(target= user_handle, args=(client_sock, client_address))
        server_thread.start()
        
if __name__ == "__main__":
    main()
    
