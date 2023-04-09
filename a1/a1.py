import threading
import socket
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a new socket with the library above. The parameters in the brackets are 
                                                        # AF_IFNET - address family, SOCK_STREAM - socket type. 
                                                        # The parameters specify the network-layer and transport- layer protocol.
user_name = ""
name_list = ""
txt_input = []
txt_cmd = ""
txt_msg = ""
user_logged = False

def send_func(command, msg, sock): # function that sends user input and/or preceeding commands to server
    while True: #FIXME temporary, makes the thread run untill it is ended
        message_to_send = command + msg + "\n"
        string_bytes = message_to_send.encode("utf-8")

        global txt_input
        txt_input = [] # reinitializes list to empty
        txt_input = msg.split(" ", 2) # splits message from the first space (command) + (msg)

        bytes_len = len(string_bytes)
        num_bytes_to_send = bytes_len

        while num_bytes_to_send > 0:
            num_bytes_to_send -= sock.send(string_bytes[bytes_len-num_bytes_to_send:])

def user_cmd(): # cmmds list: !quit = quits program, !who = shows list of online users, @username message = receiver and message
    global txt_input
    if (txt_input[0] == "!quit"):
        print(0)
        #FIXME implement a quit from the server
    elif(txt_input[0] == "!who"):
        print(0)
        #FIXME implement a link to the list function
        curr_names_list()
    elif("@" in txt_input[0]):
        print(0)
        #FIXME link to the send message + select user function(s)
    else:
        print("Command unknown. Type in !help for a list of commands.\n")
        #FIXME implement a help function that shows a list of commands
        
def curr_names_list():
    global sock
    send_func("","LIST", sock) # requests for all currently logged users
    global name_list 
    name_list = sock.recv(4096) # stores response in a global variable
     

def send_shake():
    try: 
        global user_name, sock
        user_name = input("What's your username?\n")
        send_func("HELLO-FROM ", user_name, sock)
        
    except OSError as msg: # exception catch
        print(msg)
        
def recv_func(sock):
    while True: #FIXME temporary, makes the thread run untill it is ended
        try: 
            # Waiting until data comes in 
            data = sock.recv(4096) # Receive at most 4096 bytes. 
            if data:
                print(data)
                global user_logged
                user_logged = True
                curr_names_list()
                #FIXME make the program if connect works
            else:
                if not data:
                    print("Server is closed")
                elif(data == "BUSY\n"):
                    print("Sorry, maximum numbers of users exceeded. Please try again later\n")
                    #FIXME add a quick shortcut to QUIT func
                elif(data == "IN-USE\n"):
                    print("Current username is in use.\n")
                    main()
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

#def send_msg():
    

def main():
         
    host_port = ("143.47.184.219", 5378) # port used to connect to the vu chat server
    global sock
    sock.connect(host_port)
    
    send_thread = threading.Thread(target=send_shake,)
    recv_thread = threading.Thread(target=recv_func, args=(sock,))
    send_thread.start(), recv_thread.start()
    send_thread.join(), recv_thread.join()
    
    sock.close()
    
if __name__ == "__main__":
    main()
#s.close() - to close? 