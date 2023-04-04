import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a new socket with the library above. The parameters in the brackets are 
                                                        # AF_IFNET - address family, SOCK_STREAM - socket type. 
                                                        # The parameters specify the network-layer and transport- layer protocol.

host_port = ("143.47.184.219", 5378) # port used to connect to the vu chat server
sock.connect(host_port)


