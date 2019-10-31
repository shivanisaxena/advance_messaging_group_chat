import socket, select, string, sys

#Helper function (formatting)
def display() :
	you="\33[33m\33[1m"+" You: "+"\33[0m"
	sys.stdout.write(you)
	sys.stdout.flush()

def main():

    
    host = socket.gethostname()
    port = 5010
    
    #ask for group id
    q='''\33[32m\r\33[1m which group you want to join?
 Enter the following id for joining group:
    press 1 for group MACHINE_LEARNING
    press 2 for group NATURAL_LANGUAGE_PROCESSING'''
    print(q)
    group_id=(input())

    #asks for user name
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    # connecting host
    try :
        s.connect((host, port))
    except :
        print("\33[31m\33[1m Can't connect to the server \33[0m")
        sys.exit()

    #if connected
    s.send(group_id.encode())
    display()
    option=input("your option\n 1.sign up\n 2.sign in\n")
    s.send(option.encode())
    name=input("\33[34m\33[1m\nEnter username: \33[0m")
    s.send(name.encode())
    while 1:
        socket_list = [sys.stdin, s]
        
        # Get the list of sockets which are readable
        rList, wList, error_list = select.select(socket_list , [], [])
        
        for sock in rList:
            #incoming message from server
            if sock == s:
                data = sock.recv(8000)
                if not data :
                    print("\33[31m\33[1m \rDISCONNECTED!!\n \33[0m")
                    sys.exit()
                else :
                    sys.stdout.write(str(data.decode()))
                    display()
        
            #user entered a message
            else :
                display()
                msg=sys.stdin.readline()
                msg.rstrip('\n')
                s.send(msg.encode())

if __name__ == "__main__":
    main()
