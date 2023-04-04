import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a new socket with the library above. The parameters in the brackets are 
                                                        # AF_IFNET - address family, SOCK_STREAM - socket type. 
                                                        # The parameters specify the network-layer and transport- layer protocol.

host_port = ("143.47.184.219", 5378) # port used to connect to the vu chat server
sock.connect(host_port)

def send_shake():
    try: 
        user_name = "alpha"

        message_to_send = "HELLO-FROM " + user_name
        string_bytes = message_to_send.encode("utf-8")

        bytes_len = len(string_bytes)
        num_bytes_to_send = bytes_len

        while num_bytes_to_send > 0:
            # send returns the number of bytes that were sent.
            num_bytes_to_send -= sock.send(string_bytes[bytes_len-num_bytes_to_send:]) # sends the remaining bytes, if needed until 0
    
    except OSError as msg: # exception catch
        print(msg)
        
def recv_shake():
    try: 
         # Waiting until data comes in 
        data = sock.recv(4096) # Receive at most 4096 bytes. 

        if not data:
            print("Server is closed")
        elif(data == "BUSY\n"):
            print("Sorry, maximum numbers of users exceeded. Please try again later/n")
            #FIXME maybe add a quick shortcut to QUIT func?
        elif(data == "IN-USE/n"):
            print("Current username is in use. Enter a new one:/n")
            #FIXME add a way for user to add new name
        
    except OSError as msg:
        print(msg)
            
          