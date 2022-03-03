import socket
import time
import string
import random

from locust import Locust, TaskSet, events, task, between

		
class UserBehavior(TaskSet):

	
	@task(2)
	def short_send(self):
		start_time = time.time()
		response = ''
		try:			
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				sock.connect((self.locust.host, 55312))
				uName = sock.recv(1024)

				userName = "one"
				sock.send(userName.encode())
				
				inMsg = 'Mary had a little lamb'
				
				sock.send(inMsg.encode())
        
		except Exception as e:
			total_time = int(time.time() - start_time) * 1000
			events.request_failure.fire(request_type='msgSend',
										name='short_Exception',
										response_time=total_time,
										response_length=0,
										exception=e)
		else:
			total_time = int(time.time() - start_time) * 1000
			events.request_success.fire(request_type='msgSend',
										name='short_Success',
										response_time=total_time,
										response_length=len(response))

	@task(2)
	def msg_help(self):
		start_time = time.time()
		response = ''
		try:			
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				sock.connect((self.locust.host, 55312))
				uName = sock.recv(1024)

				userName = "two"
				sock.send(userName.encode())
				
				inMsg = '/help'
				
				sock.send(inMsg.encode())
        
		except Exception as e:
			total_time = int(time.time() - start_time) * 1000
			events.request_failure.fire(request_type='msgHelp',
										name='help_Exception',
										response_time=total_time,
										response_length=0,
										exception=e)
		else:
			total_time = int(time.time() - start_time) * 1000
			events.request_success.fire(request_type='msgHelp',
										name='help_Success',
										response_time=total_time,
										response_length=len(response))										

	@task(2)
	def msg_participants(self):
		start_time = time.time()
		response = ''
		try:			
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				sock.connect((self.locust.host, 55312))
				uName = sock.recv(1024)

				userName = "three"
				sock.send(userName.encode())
				
				inMsg = '/p'
				
				sock.send(inMsg.encode())
        
		except Exception as e:
			total_time = int(time.time() - start_time) * 1000
			events.request_failure.fire(request_type='msgParticipants',
										name='participants_Exception',
										response_time=total_time,
										response_length=0,
										exception=e)
		else:
			total_time = int(time.time() - start_time) * 1000
			events.request_success.fire(request_type='msgParticipants',
										name='participants_Success',
										response_time=total_time,
										response_length=len(response))
										
	@task(2)
	def change_name(self):
		start_time = time.time()
		response = ''
		try:			
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				sock.connect((self.locust.host, 55312))
				uName = sock.recv(1024)

				userName = "four"
				sock.send(userName.encode())
				
				inMsg = '/ch'
				
				sock.send(inMsg.encode())
				
				_LENGTH = 5
				string_pool = string.ascii_lowercase
				result = ""
				for i in range(_LENGTH) :
					result += random.choice(string_pool)
				
				sock.send(result.encode())
        
		except Exception as e:
			total_time = int(time.time() - start_time) * 1000
			events.request_failure.fire(request_type='changeName',
										name='changename_Exception',
										response_time=total_time,
										response_length=0,
										exception=e)
		else:
			total_time = int(time.time() - start_time) * 1000
			events.request_success.fire(request_type='changeName',
										name='changename_Success',
										response_time=total_time,
										response_length=len(response))
										
	@task(2)
	def long_send(self):
		start_time = time.time()
		response = ''
		try:			
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				sock.connect((self.locust.host, 55312))
				uName = sock.recv(1024)

				userName = "five"
				sock.send(userName.encode())
				
				inMsg = 'Mary had a little lamb'
								
				for i in range(random.randint(20, 100)):
					sock.send(inMsg.encode())
        
		except Exception as e:
			total_time = int(time.time() - start_time) * 1000
			events.request_failure.fire(request_type='msgSend',
										name='long_Exception',
										response_time=total_time,
										response_length=0,
										exception=e)
		else:
			total_time = int(time.time() - start_time) * 1000
			events.request_success.fire(request_type='msgSend',
										name='long_Success',
										response_time=total_time,
										response_length=len(response))


class SocketUser(Locust):

	host = 'localhost'

	task_set = UserBehavior

	wait_time = between(1, 3)