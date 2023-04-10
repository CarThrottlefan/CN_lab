import threading
import socket
import select

sock = 0

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a new socket with the library above. The parameters in the brackets are 
                                                        # AF_IFNET - address family, SOCK_STREAM - socket type. 
                                                        # The parameters specify the network-layer and transport- layer protocol.
user_name = ""
name_list = []
txt_input = []
txt_cmd = ""
txt_msg = ""
user_logged = False

def send_func(command, msg, sock): # function that sends user input and/or preceeding commands to server
    #while True: #FIXME temporary, makes the thread run untill it is ended
        message_to_send = command + msg + "\n"
        string_bytes = message_to_send.encode("utf-8")
        
        bytes_len = len(string_bytes)
        num_bytes_to_send = bytes_len

        while num_bytes_to_send > 0:
            num_bytes_to_send -= sock.send(string_bytes[bytes_len-num_bytes_to_send:])

def user_cmd(): # cmmds list: !quit = quits program, !who = shows list of online users, @username message = receiver and message
    global txt_input, txt_cmd, txt_msg #FIXME Not tested, not sure if they will work
    user_cmds = input("Input a command, or type in !help for a list of commands.\n")
    txt_input = user_cmds.split(" ", 2)  # splits message from the first space (command) + (msg)
    txt_cmd = txt_input[0]
    if (len(txt_input) > 1):
        txt_msg = txt_input[1]
    if (txt_cmd == "!quit"):
        print(1)
        sock.close()
        #FIXME implement a quit from the server
    elif(txt_cmd == "!who"):
        print(2)
        get_list = threading.Thread(target=curr_names_list,)
        get_list.start(), get_list.join()
        #FIXME implement a link to the list function
        #curr_names_list()
    elif("@" in txt_cmd):
        print()
        #FIXME link to the send message + select user function(s)
    else:
        print("Command unknown. Type in !help for a list of commands.\n")
        #FIXME implement a help function that shows a list of commands
        
def curr_names_list():
    print('namelist')
    global sock
    send_func("","LIST", sock) # requests for all currently logged users
    global name_list 
    name_list = sock.recv(4096)# stores response in a global variable
    print(name_list)
     

def send_shake():
    try: 
        global user_name, sock
        user_name = input("What's your username?\n")
        send_func("HELLO-FROM ", user_name, sock)
        
    except OSError as msg: # exception catch
        print(msg)
        
def recv_func(sock):
    #while True: #FIXME temporary, makes the thread run untill it is ended
        try: 
            # Waiting until data comes in 
            data = sock.recv(4096) # Receive at most 4096 bytes. 
            if(data == b"BUSY\n"):
                print("Sorry, maximum numbers of users exceeded. Please try again later\n")
                #FIXME add a quick shortcut to QUIT func
            elif(data == b"IN-USE\n"):
                print("Current username is in use.")
                main()
            #elif (data == "":
                #chat_error(data)
            elif data:
                print(0)
                print(data)
                global user_logged
                user_logged = True
                user_cmd()
                #FIXME make the program if connect works
            #else:
                #idk
            
        except OSError as msg:
            print(msg)
            
def chat_error(data):  
    
    if(data == b"BAD-DEST-USER\n"):
        print("The user you are trying to reach is currently offline. Want to select another one?\n")
        # FIXME prompt user to select new user from list
    # elif(data == b"BAD-RQST-HDR\n"):
        # FIXME find a way to fix broken header
    # elif(data == b"BAD-RQST-BODY\n"):
        # FIXME find a way to fix broken body
    else:
        print("An unknown error has occured.\n")

#def send_msg():
    

def main():
    
    global sock
    print('main')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
    host_port = ("143.47.184.219", 5378) # port used to connect to the vu chat server
    sock.connect(host_port)
    
    
    send_thread = threading.Thread(target=send_shake,)
    recv_thread = threading.Thread(target=recv_func, args=(sock,))
    send_thread.start(), recv_thread.start()
    send_thread.join(), recv_thread.join()
    
    #sock.close()
    
    #sock.connect(host_port)
    
    
if __name__ == "__main__":
    main()
#s.close() - to close? 