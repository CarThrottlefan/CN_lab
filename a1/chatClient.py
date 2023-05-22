import socket
import threading 
import re
import os


def send(sock, msg):
    """Sends entire message over socket."""

    string_bytes = (msg + '\n').encode("utf-8", "replace")
    bytes_len = len(string_bytes)
    num_bytes_to_send = bytes_len

    while num_bytes_to_send > 0:
        num_bytes_to_send -= sock.send(string_bytes [bytes_len - num_bytes_to_send:])

buffer = ''

def recv(sock):
    """Waits until entire message is received from server (until \\n) and returns it"""

    global buffer

    while True:
        if '\n' in buffer:
            break

        data = sock.recv(4096)

        if not data:
            os._exit(1) # kills main program, regardless if inside thread or not

        buffer += data.decode("utf-8") #reads chunks of data and puts them into the buffer
    
    # extract message (delimited by \n) from buffer
    msg = buffer[:buffer.find('\n')] #extracts the first message from the buffer
    buffer = buffer[buffer.find('\n') + 1:] #leaves the rest of the buffer alone for now

    return msg

# DELIVER

host_port = ("192.168.50.143", 8231)

msg = ""

while not msg.startswith("HELLO"):
    name = input("Enter your name: ")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(host_port)
    send(sock, "HELLO-FROM " + name)
    msg = recv(sock)

    if msg == "IN-USE":
        print("Name already in use, please try again!")


def receive():
    while True:
        try:
            msg = recv(sock) # function is blocking, reads the most recent message, will not return until it has the most recent message
        
            match msg:
                case msg if msg.startswith("LIST-OK "):
                    print(f"Logged on users: {msg.split()[1]}")
                
                case "SEND-OK":
                    print("Message sent successfully")

                case "BAD-DEST-USER":
                    print("Unknown user")
                
                case msg if msg.startswith("DELIVERY "):
                    msg = msg.split(" ", 2)

                    print(f"Message from @{msg[1]}: {msg[2]}")
                
                case "BAD-RQST-HDR":
                    print("Wrong command")
                
                case "BAD-RQST-BODY":
                    print("Message must contain text")
                
                case msg:
                    print(msg)
        
        except OSError as e:
            print("Error: " + e)


def write():
    while True:
        line = input("> ")

        msg_pattern = re.compile(r"@(\S+) (.*)")

        match line:
            case "!quit":
                os._exit(0)

            case "!who":
                send(sock, "LIST")

            case msg if msg_pattern.match(msg):
                m = msg_pattern.match(msg)

                send(sock, f"SEND {m.group(1)} {m.group(2)}")

            case _:
                print("Invalid command!")
            #case msg: #simulates a "Bad Header request"
                #send(sock, msg)
            #case msg: #simulates a "Bad Body request"
                #m = msg_pattern.match(msg)
                #send(sock, 'SEND Alex')
            


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()