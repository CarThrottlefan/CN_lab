import threading
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a new socket with the library above. The parameters in the brackets are 
                                                        # AF_IFNET - address family, SOCK_STREAM - socket type. 
                                                        # The parameters specify the network-layer and transport- layer protocol.
user_name = ""
name_list = ""
txt_command = ""

def send_func(command, msg): # function that sends user input and/or preceeding commands to server
    message_to_send = command + msg + "\n"
    string_bytes = message_to_send.encode("utf-8")

    bytes_len = len(string_bytes)
    num_bytes_to_send = bytes_len

    while num_bytes_to_send > 0:
            sock.setblocking(1)
            num_bytes_to_send -= sock.send(string_bytes[bytes_len-num_bytes_to_send:])
    if(num_bytes_to_send == 0):
        sock.setblocking(0)

def user_cmd(): # cmmds list: !quit = quits program, !who = shows list of online users, @username message = receiver and message
    global txt_input
    if (txt_input == "!quit"):
        print(0)
        #FIXME implement a quit from the server
    elif(txt_input == "!who"):
        print(0)
        #FIXME implement a link to the list function
    elif("@" in txt_input):
        print(0)
        #FIXME link to the send message + select user function(s)
    else:
        print("Command unknown. Type in !help for a list of commands.\n")
        #FIXME implement a help function that shows a list of commands
def curr_names_list():
    send_func("","LIST") # requests for all currently logged users
    global name_list 
    name_list = sock.recv(4096) # stores response in a global variable
     

def send_shake():
    try: 
        global user_name
        user_name = input("What's your username?\n")
        send_func("HELLO-FROM ", user_name)
        
    except OSError as msg: # exception catch
        print(msg)
        
def recv_shake():
    try: 
         # Waiting until data comes in 
        data = sock.recv(4096) # Receive at most 4096 bytes. 
        if data:
            print(data)
            #FIXME make the program if connect works
        else:
            if not data:
                print("Server is closed")
            elif(data == "BUSY\n"):
                print("Sorry, maximum numbers of users exceeded. Please try again later\n")
                #FIXME add a quick shortcut to QUIT func
            elif(data == "IN-USE\n"):
                print("Current username is in use.\n")
                host_port = ("143.47.184.219", 5378)
                sock.connect(host_port)
                send_shake()
                #FIXME add a way for user to add new name - WORKING?
            elif data:
                chat_error(data)
        
    except OSError as msg:
        print(msg)
            
def chat_error(data):  
    
    if(data == "BAD-DEST-USER\n"):
        print("The user you are trying to reach is currently offline. Want to select another one?\n")
        # FIXME prompt user to select new user from list
    # elif(data == "BAD-RQST-HDR\n"):
        # FIXME find a way to fix broken header
    # elif(data == "BAD-RQST-BODY\n"):
        # FIXME find a way to fix broken body
    else:
        print("An unknown error has occured.\n") 

         
host_port = ("143.47.184.219", 5378) # port used to connect to the vu chat server
sock.connect(host_port)
send_thread = threading.Thread(target=send_shake, args=(command, msg))
send_shake(), recv_shake()