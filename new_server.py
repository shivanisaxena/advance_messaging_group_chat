import socket, select
from _thread import *
import os

#Function to send message to all connected clients
def send_to_all (sock,l, message):
	#Message not forwarded to server and sender itself
	for socket in connected_lists[l]:
		if socket != server_socket and socket != sock :
			try :
				socket.send(message.encode('utf-8'))
			except :
				# if connection not available
				socket.close()
				connected_lists[l].remove(socket)
				connected_list.remove(socket)
def choices(l,sock,option):
	if option2==1:
		list_file()
	if option2==2:
		upload_file()
	if option2==3:
		download_file()
	if option2==4:
		delete_file()
	if option2==5:
		share_file()
	if option2==6:
		show_log()
	
	if option2==8:
								
		(i,p)=sock.getpeername()
		if l==1:
			send_to_all(sock,l, "\r\33[31m \33[1m"+str(record1[(i,p)])+" left the conversation\33[0m\n")
			print("Client (%s, %s) is offline (error)" % (i,p)," [",record1[(i,p)],"]\n")
			del record1[(i,p)]
		if l==2:
			send_to_all(sock,l, "\r\33[31m \33[1m"+str(record2[(i,p)])+" left the conversation\33[0m\n")
			print("Client (%s, %s) is offline (error)" % (i,p)," [",record2[(i,p)],"]\n")
			del record2[(i,p)]
		connected_list.remove(sock)
		connected_lists[l].remove(sock)
		sock.close()
		



def client_thread(l,sock):
		
			while True:
				try:
					data1 = sock.recv(buffer)
					# print("sock is:",sock)
					
					data=str(data1.decode())
					print("\ndata received:",data)
					print("\ndata=",data1.decode())
                    
                    #get addr of client sending the message
					(i,p)=sock.getpeername()
					if data =='':
						if l==1:
							msg="\r\33[1m"+"\33[31m "+str(record1[(i,p)])+" left the conversation \33[0m\n"
							send_to_all(sock,l,msg)
						if l==2:
							msg="\r\33[1m"+"\33[31m "+str(record2[(i,p)])+" left the conversation \33[0m\n"
							send_to_all(sock,l,msg)
						if l==1:
							print("Client (%s, %s) is offline" % (i,p)," [",record1[(i,p)],"]")
							del record[(i,p)]
						if l==2:
							print("Client (%s, %s) is offline" % (i,p)," [",record2[(i,p)],"]")
							del record[(i,p)]
						connected_list.remove(sock)
						connected_lists[l].remove(sock)
						sock.close()
						continue

					else:
						if l==1:
							msg="\r\33[1m"+"\33[35m "+str(record1[(i,p)])+": "+"\33[0m"+data+"\n"
						if l==2:
							msg="\r\33[1m"+"\33[35m "+str(record2[(i,p)])+": "+"\33[0m"+data+"\n"
						send_to_all(sock,l,msg)
            
                #abrupt user exit
				except:
					(i,p)=sock.getpeername()
					if l==1:
						send_to_all(sock,l, "\r\33[31m \33[1m"+str(record1[(i,p)])+" left the conversation unexpectedly\33[0m\n")
						print("Client (%s, %s) is offline (error)" % (i,p)," [",record1[(i,p)],"]\n")
						del record1[(i,p)]
					if l==2:
						send_to_all(sock,l, "\r\33[31m \33[1m"+str(record2[(i,p)])+" left the conversation unexpectedly\33[0m\n")
						print("Client (%s, %s) is offline (error)" % (i,p)," [",record2[(i,p)],"]\n")
						del record2[(i,p)]
					connected_list.remove(sock)
					connected_lists[l].remove(sock)
					sock.close()
					continue
		


if __name__ == "__main__":
	name=""
	#dictionary to store address corresponding to username
	record1={}
	record2={}
	# List to keep track of socket descriptors
	connected_lists = []
	for k in range(1,4):
		connected_lists.append([])
	connected_list =[]
	buffer = 4096
	port = 5010

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((socket.gethostname(), port))
	server_socket.listen(10) #listen atmost 10 connection at one time

	# Add server socket to the list of readable connections
	connected_list.append(server_socket)
	for k in range(3):
		connected_lists[k].append(server_socket)

	print("\33[32m \t\t\t\tSERVER WORKING \33[0m")
	
	while 1:
        # Get the list sockets which are ready to be read through select
		rList,wList,error_sockets = select.select(connected_list,[],[])
		
		for sock in rList:
			#New connection
			if sock == server_socket:
				# Handle the case in which there is a new connection recieved through server_socket
				sockfd, addr = server_socket.accept()
				name1=sockfd.recv(buffer)
				name1=name1.decode()
				l=int(name1)
				connected_lists[l].append(sockfd)
				connected_list.append(sockfd)
				sockfd.send("\33[32m\r\33[1m Welcome and Hii....\n\33[0m".format(l).encode())
				option=sockfd.recv(buffer)
				option=option.decode()
				option=int(option)
				
				name=sockfd.recv(buffer)
				name=name.decode()
				
				#print("record and conn list ",record,connected_list)
                
                #if repeated username
				if l==1 and option==2:
					record1[addr]=""
					f=open("accountfile1.txt","r")
					lines=f.readlines()# Read the lines
					f.close()
					flag1=0
					for line in lines:
						if name in line:
							flag1=1
					if flag1==1:
                                                        sockfd.send("\33[32m\r\33[1m welcome back to the group MACHINE LEARNING\n\33[0m".encode())
                                                        record1[addr]=name
                                                        print("Client (%s, %s) connected" % addr," [",record1[addr],"]")
                                                        send_to_all(sockfd,l, "\33[32m\33[1m\r "+str(name)+" joined the conversation \n\33[0m")
                                                        sockfd.send("\33[36m\r\33[1m What you wnat to do?\n 1.List files\n2.Upload files\n3.Download files\n4.Delete file\n5.Share file\n6.Show log\n7.chat\n8.sign out\n\33[0m".encode())
                                                        option2=sockfd.recv(buffer)
                                                        
                                                        option2=int(option2)
                                                        if option2==7:
                                                        	start_new_thread(client_thread,(l,sockfd,))
                                                        else:
                                                        	choices(l,sockfd,option2)                                                       
					else:
                                                        sockfd.send("\33[31m\33[1m \r              username does not exist\33[0m".encode())
                                                        f.close()
                                                        del record1[addr]
                                                        connected_lists[l].remove(sockfd)
                                                        connected_list.remove(sockfd)
                                                        sockfd.close()
                                                        continue
					


				if l==1 and option==1:
					record1[addr]=""
					f=open("accountfile1.txt","r")
					lines=f.readlines()# Read the lines
					f.close()
					flag1=0
					for line in lines:
						if name in line:
							flag1=1
					if flag1==1:
                                                        sockfd.send("\33[31m\33[1m \r              username already exixts\33[0m".encode())
                                                        del record1[addr]
                                                        connected_lists[l].remove(sockfd)
                                                        connected_list.remove(sockfd)
                                                        sockfd.close()
                                                        continue
						
								
				if l==2 and option==2:
					record2[addr]=""
					f=open("accountfile2.txt","r")
					lines=f.readlines()
					f.close()
					flag2=0
					for line in lines:# Split on the space, and store the results in a list of two strings
						if name in line:
							flag2=1
					if flag2==1:
                                                        sockfd.send("\33[32m\r\33[1m Welcome back to the group NATURAL LANGUAGE PROCESSING\n\r\33[0m".encode())
                                                        record2[addr]=name
                                                        print("Client (%s, %s) connected" % addr," [",record2[addr],"]")
                                                        
                                                        send_to_all(sockfd,l, "\33[32m\33[1m\r "+str(name)+" joined the conversation \n\33[0m")
                                                        sockfd.send("\33[36m\r\33[1m What you wnat to do?\n 1.List files\n2.Upload files\n3.Download files\n4.Delete file\n5.Share file\n6.Show log\n7.chat\n8.sign out\n\33[0m".encode())
                                                        option2=sockfd.recv(buffer)
                                                        
                                                        option2=int(option2)
                                                        if option2==7:
                                                        	start_new_thread(client_thread,(l,sockfd,))
                                                        else:
                                                        	choices(l,sock,option2)
					else:
                                                        sockfd.send("\33[31m\33[1m \r              username does not exist\33[0m".encode())
                                                        f.close()
                                                        del record2[addr]
                                                        connected_lists[l].remove(sockfd)
                                                        connected_list.remove(sockfd)
                                                        sockfd.close()
                                                        continue
					


				if l==2 and option==1:
					record2[addr]=""
					f=open("accountfile2.txt","r")
					lines=f.readlines()
					f.close()
					flag2=0
					for line in lines:
						if name in line:
							flag2=1
					if flag2==1:
                                                        sockfd.send("\33[31m\33[1m \r               username already exixts\33[0m".encode())
                                                        f.close()
                                                        del record2[addr]
                                                        connected_lists[l].remove(sockfd)
                                                        connected_list.remove(sockfd)
                                                        sockfd.close()
                                                        continue
					
						
								
	

				
				              
                    #add name and address
				if l==1 and flag1==0:
						
						files=open("accountfile1.txt","a")
						files.write(name)
						files.write("\n")
						files.close()
						record1[addr]=name
						print("Client (%s, %s) connected" % addr," [",record1[addr],"]")
						sockfd.send("\33[32m\r\33[1m WELCOME TO THE WORLD OF MACHINE LEARNING\n\33[0m".encode())
						send_to_all(sockfd,l, "\33[32m\33[1m\r "+str(name)+" joined the conversation \n\33[0m")
						sockfd.send("\33[36m\r\33[1m What you wnat to do?\n 1.List files\n2.Upload files\n3.Download files\n4.Delete file\n5.Share file\n6.Show log\n7.chat\n8.sign out\n\33[0m".encode())
						option2=sockfd.recv(buffer)
						
						option2=int(option2)
						if option2==7:
                                                        	start_new_thread(client_thread,(l,sockfd,))
						else:
							choices(l,sock,option2)

				if l==2 and flag2==0:
					
						files=open("accountfile2.txt","a")
						files.write(name)
						files.write("\n")
						files.close()
						record2[addr]=name
						print("Client (%s, %s) connected" % addr," [",record2[addr],"]")
						sockfd.send("\33[32m\r\33[1m WELCOME TO THE WORLD OF NATURAL LANGUAGE PROCESSING\n\33[0m".encode())
						send_to_all(sockfd,l, "\33[32m\33[1m\r "+str(name)+" joined the conversation \n\33[0m")
						
				
						sockfd.send("\33[36m\r\33[1m What you wnat to do?\n 1.List files\n2.Upload files\n3.Download files\n4.Delete file\n5.Share file\n6.Show log\n7.chat\n8.sign out\n\33[0m".encode())
						option2=sockfd.recv(buffer)
						
						option2=int(option2)
						if option2==7:
                                                        	start_new_thread(client_thread,(l,sockfd,))
						else:
							choices(l,sock,option2)
						
			#Some incoming message from a client
			
				
	server_socket.close()                  


