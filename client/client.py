from socket import *
import threading

HOST = 'localhost'
PORT = 55312
ADDR = (HOST, PORT)

mysock = socket(AF_INET, SOCK_STREAM)
print("Connecting to server {} on port {}...".format(HOST, PORT))

def startClient():

	try: 
		mysock.connect(ADDR)
		print("Connection Complete.")

	except Exception as e:
		print(e)
	
	uName = mysock.recv(1024)

	try:
		userName = input("{} ".format(uName.decode()))

		if userName == '':
			while userName == '':
				print('Blank is not allowed.')
				print("If you don't want to join this chat, enter 'Ctrl-C'.")
				try:
					userName = input("{} ".format(uName.decode()))
				except KeyboardInterrupt:
					print("\nProgram is terminated because of 'Ctrl+C' key.")
					mysock.shutdown(SHUT_RDWR)
					mysock.close()
					return 3

	except KeyboardInterrupt:
		print("Program is terminated because of 'Ctrl+C' key.")
		mysock.shutdown(SHUT_RDWR)
		mysock.close()
		return 3
		
	else:
		mysock.send(userName.encode())
		return 2

def receive():
	global mysock
	while True:
		try:
			data = mysock.recv(1024)
			
		except ConnectionError:
			print("Disconnected from the server. Press the Enter key.")
			break
			
		except KeyboardInterrupt:
			print("Program is terminated because of 'Ctrl+C' key.")
			break
			
		if not data:
			print("You have successfully logged out of the server.")
			break
			
		print(data.decode("UTF-8"))
	mysock.shutdown(SHUT_RD)
		
def mainthread():
	global mysock
	thread_recv = threading.Thread(target = receive, args = ())
	thread_recv.start()
	while True:
		try:
			data = input("")
			
		except EOFError:
			print("Program is terminated because of 'EOFError'.")
			break
			
		except KeyboardInterrupt:
			print("Program is terminated because of 'Ctrl+C' key.")
			break
			
		if data == '/quit':
			print("Program is terminated because of '/quit'.")
			print("Disconnecting from server.")
			break
			
		try:
			data = data + "\n"
			mysock.send(bytes(data, "UTF-8"))
			
		except ConnectionError:
			print("Disconnecting from server.")
			break
			
		except KeyboardInterrupt:
			print("Program is terminated because of 'Ctrl+C' key.")
			break
			
	print("Close the write buffer on the socket.")
	mysock.shutdown(SHUT_WR)
	thread_recv.join()
	
	
flagnum = startClient()

if flagnum == 2:

	thread_main = threading.Thread(target = mainthread, args = ())
	thread_main.daemon = True
	thread_main.start()
	
	try:
		thread_main.join()
		
	except KeyboardInterrupt:
		print("Program is terminated because of 'Ctrl+C' key.")
		mysock.close()
		print("Close the socket.")
		print("The client program ended successfully.")
	
	else:
		mysock.close()
		print("Close the socket.")
		print("The client program ended successfully.")
	
elif flagnum == 3:
	print("\nClose the socket.")
	print("The client program ended successfully.")
