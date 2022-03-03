import socketserver
import threading

HOST = ''
PORT = 55312
lock = threading.Lock()

class UserHandler:

	def __init__(self):
		self.users = {}

	def makeUser(self, username, conn, addr):
		if username in self.users:
			conn.send('This is already a registered user.\n'.encode())
			return None

		lock.acquire() 
		self.users[username] = (conn, addr)
		lock.release() 

		self.sendMessageToAll('[%s] has entered.\n' %username)
		print('+++ Number of participants [%d]' %len(self.users))
		return username

	def deleteUser(self, username): 
		if username not in self.users:
			return

		lock.acquire()
		del self.users[username]
		lock.release()

		self.sendMessageToAll('[%s] has left.\n' %username)
		print('--- Number of participants [%d]' %len(self.users))

	def messageProcess(self, username, msg): 
		if msg.strip() == '/quit': 
			self.deleteUser(username)
			return -1
		else:
			if msg.strip() == '/w':
				return 5
			if msg.strip() == '/p':
				return 4
			if msg.strip() == '/ch':
				return 3
			if msg.strip() == '/help':
				return 2
			if msg.strip() == '/candy':
				candy = '>(//)<\n'
				self.sendMessageToAll('[%s] %s\n' %(username, candy))
				return 1
			if msg.strip() == '/smile':
				smile = '(^o^)\n'
				self.sendMessageToAll('[%s] %s' %(username, smile))
				return 1 	
			if msg.strip() == '/good':
				good = '(*^___^*)b \n'
				self.sendMessageToAll('[%s] %s' %(username, good))
				return 1 
			if msg.strip() == '/love':
				love = '\n ** **\n*  *  *\n*     *\n *   *\n  * *\n   *\n'
				self.sendMessageToAll('[%s] %s' %(username, love))
				return 1 				
			if msg.strip() == '/amaze':
				amaze = "( 'o' )\n"
				self.sendMessageToAll('[%s] %s' %(username, amaze))
				return 1 	
			if msg.strip() == '/sad':
				sad = '(T^T)\n'
				self.sendMessageToAll('[%s] %s' %(username, sad))
				return 1 	
			if msg.strip() == '/angry':
				angry = '(-_-)a\n'
				self.sendMessageToAll('[%s] %s' %(username, angry))
				return 1 	
			if msg.strip() == '/sleepy':
				sleepy = '(-.-)Zzz\n'
				self.sendMessageToAll('[%s] %s' %(username, sleepy))
				return 1 					
			self.sendMessageToAll('[%s] %s' %(username, msg))			
			return			
	
	def changename(self, conn, name, input_name, addr):
		global new_name
		new_name = input_name
		
		if name == input_name:
			return name
		if new_name in self.users:
			return name
		
		lock.acquire() 
		self.users[new_name] = self.users[name]
		del self.users[name]
		lock.release()
		
		chmsg1 = "Your new name is " + "[" + new_name + "].\n"
		chmsg2 = "The New Name of [" + name +  "] is [" + new_name + "].\n"
		
		conn.send(chmsg1.encode())
		self.sendMessageToAll(chmsg2)
		print(chmsg2)
		return new_name
	
	def sendMessageToAll(self, msg):
		for conn, addr in self.users.values():
			conn.send(msg.encode())
		
	def awayMsg(self, conn, name, wname, wmsg):
		A_conn, A_addr = self.users[wname]
		nmsg = ' (W) [' + name + '] ' + wmsg + '\n'
		A_conn.send(nmsg.encode())
		conn.send(nmsg.encode())
		print(nmsg)
		

class MyTcpHandler(socketserver.BaseRequestHandler):
	userman = UserHandler()
	
	def handle(self): 
		print('[%s] address is connected.' %self.client_address[0])
		username = ''

		try:
			username = self.registerUser()
			self.request.send('--------------------------------------------------------------\n'.encode())	
			self.request.send('"/quit" : quit this chatroom.\n'.encode())
			self.request.send('"/help" : see this explanation again.\n'.encode())
			self.request.send('"/ch" : change your name.\n'.encode())
			self.request.send('"/p" : see all participants in chat room.\n'.encode())
			self.request.send('"/w" : send secret messages to a participant.\n'.encode())
			self.request.send("       This secret message can't use emoji.\n".encode())
			self.request.send('"/(word)" : type some word you can use emoji.\n   word : candy, smile, good, love, amaze, sad, angry, sleepy\n'.encode())
			self.request.send('--------------------------------------------------------------\n'.encode())
			numbermsg = 'Number of participants [' + str(len(self.userman.users)) + ']\n'
			self.request.send(numbermsg.encode())
			msg = self.request.recv(1024)
			
			while msg:
				print("[" + username + "]" + msg.decode())
				checknum = self.userman.messageProcess(username, msg.decode())
				if checknum == -1:
					self.request.close()
					break
				if checknum == 2:
					self.request.send('--------------------------------------------------------------\n'.encode())	
					self.request.send('"/quit" : quit this chatroom.\n'.encode())
					self.request.send('"/help" : see this explanation again.\n'.encode())
					self.request.send('"/ch" : change your name.\n'.encode())
					self.request.send('"/p" : see all participants in chat room.\n'.encode())
					self.request.send('"/w" : send secret messages to a participant.\n'.encode())
					self.request.send("       This secret message can't use emoji.\n".encode())
					self.request.send('"/(word)" : type some word you can use emoji.\n   word : candy, smile, good, love, amaze, sad, angry, sleepy\n'.encode())
					self.request.send('--------------------------------------------------------------\n'.encode())				
				if checknum == 3:
					newName = self.changeUserName(username)							
					username = self.userman.changename(self.request, username, newName, self.client_address)
				if checknum == 4:
					smsg = '----------[' + str(len(self.userman.users)) + '] participants----------\n'
					self.request.send(smsg.encode())
					print(smsg)
					for x in self.userman.users:		
						pmsg = x + '\n'
						self.request.send(pmsg.encode())
						print(pmsg)
					self.request.send('------------------------------------\n'.encode())
					print('------------------------------------\n')
				if checknum == 5:
					wname = self.getWName(username)
					if not wname == '':
						self.request.send('Enter the message: '.encode())
						wmsg = self.request.recv(1024).decode()
						self.userman.awayMsg(self.request, username, wname, wmsg)
				
				msg = self.request.recv(1024)
			
		except Exception as e:
			print(e)

		print('[%s] connection termination' %self.client_address[0])
		if (username):
			self.userman.deleteUser(username)

	def registerUser(self):
		while True:
			self.request.send('Username:'.encode())
			username = self.request.recv(1024)
			username = username.decode().strip()
			if username == '':
				self.request.send('Blank is not allowed.\n'.encode())
				self.request.send("If you don't want to join this chat, enter 'Ctrl-C'.\n".encode())
			if not username == '':
				if self.userman.makeUser(username, self.request, self.client_address):
					return username
					
	def changeUserName(self, username):
		while True:
			self.request.send('Newname:'.encode())
			inputname = self.request.recv(1024)
			inputname = inputname.decode().strip()
			flag = 1
			if inputname == '':
				self.request.send('Blank is not allowed.\n'.encode())
				flag = 1
				while flag == 1:		
					self.request.send('Do you want to change your name? [Yes / No]  '.encode())
					ans = self.request.recv(1024).decode().strip()
					if ans == 'Yes':
						flag = 1
						break						
					elif ans == 'No':
						flag = 0
						break
					else:
						self.request.send('Please enter "Yes" or "No".\n'.encode())				
			elif inputname != '':
				if inputname == username:
					self.request.send('This is your name.\n'.encode())
					flag = 1
					while flag == 1:		
						self.request.send('Do you want to type another name? [Yes / No]  '.encode())
						ans = self.request.recv(1024).decode().strip()
						if ans == 'Yes':
							flag = 1
							break						
						elif ans == 'No':
							flag = 0
							break
						else:
							self.request.send('Please enter "Yes" or "No".\n'.encode())
				elif inputname in self.userman.users:
					self.request.send('This is already a registered user.\n'.encode())
					flag = 1
					while flag == 1:		
						self.request.send('Do you want to type another name? [Yes / No]  '.encode())
						ans = self.request.recv(1024).decode().strip()
						if ans == 'Yes':
							flag = 1
							break						
						elif ans == 'No':
							flag = 0
							break
						else:
							self.request.send('Please enter "Yes" or "No".\n'.encode())		
				else:
					return inputname					
			if flag == 0:
				return username

	def getWName(self, username):
		while True:
			self.request.send('Which user would you like to send a message to? '.encode())
			wname = self.request.recv(1024)
			wname = wname.decode().strip()
			if wname in self.userman.users:
				if wname == username:
					self.request.send('This is your name.\n'.encode())
					flag = 1
					while flag == 1:		
						self.request.send('Do you want to type another name? [Yes / No]  '.encode())
						ans = self.request.recv(1024).decode().strip()
						if ans == 'Yes':
							flag = 1
							break						
						elif ans == 'No':
							flag = 0
							break
						else:
							self.request.send('Please enter "Yes" or "No".\n'.encode())
					if flag == 0:
						return ''
						
				else:
					return wname
					
			else:
				self.request.send('This is an invalid name.\n'.encode())
				flag = 1
				while flag == 1:		
					self.request.send('Do you want to type another name? [Yes / No]  '.encode())
					ans = self.request.recv(1024).decode().strip()
					if ans == 'Yes':
						flag = 1
						break						
					elif ans == 'No':
						flag = 0
						break
					else:
						self.request.send('Please enter "Yes" or "No".\n'.encode())
				if flag == 0:
					return ''

class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass
        
def startServer():
	print('+++ Start the chat server!')
	print('+++ Press Ctrl-C to close the chat server')

	try:
		server = ChatingServer((HOST, PORT), MyTcpHandler)
		server.serve_forever()
	except KeyboardInterrupt:
		print('--- Shut down the chat server')
		server.shutdown()
		server.server_close()
	except Exception as e:
		print(e)

if __name__ == '__main__':
	print('listening on port', PORT)
	startServer()