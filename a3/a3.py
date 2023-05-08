import threading
import socket
import sys
import re
from time import sleep

serverSocket = socket.socket() 
hostName = socket.gethostname() # returns the name of the local machine
port = 8231
serverIp = (socket.gethostbyname(hostName), port) #a tuple of both the IP address of the host and the port
serverSocket.bind((hostName, port)) #assigns an IP and port to the socket

print("This is the server IP: ", serverIp)

#listen for connections
usernames = [] # list of usernames
numOfUsers = 64 # change for more users to be supported
serverSocket.listen(numOfUsers)








 

