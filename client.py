import socket
import threading
import time
import sys


max_server_count=2
server_addresses = [('192.168.122.55', 12345), ('192.168.122.56', 12346)]
is_server_alive = [True, False]           
# s = socket.socket()
# s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 ) 

server_sockets = []

def read_mode():
	with open('mode.txt', 'r') as f:
		mode = f.read()
	#print(mode)
	return mode

#Creates socket for connecting to the server, also connects if the server is up
def initialize_sockets():
	for i in range(0, max_server_count):
		server_sockets.append(socket.socket())
		server_sockets[i].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		if is_server_alive[i]:
			server_sockets[i].connect(server_addresses[i])

def handle_request_to_server():
	while True:
		for i in range(0,max_server_count):
			s = server_sockets[i]
			if is_server_alive[i]==True:
				try:
					mode = read_mode()
					if mode=="low":
						s.send(bytes('10','utf-8'))
						time.sleep(7)
					elif mode=="high":
						s.send(bytes('10','utf-8'))
						time.sleep(2)
					else:
						print("in wrong mode")
					time.sleep(2)
					print(s.recv(1024).decode('utf-8'))
				except Exception as e:
					#print('{0} while communicating'.format(e))
					is_server_alive[i] = False


def poll_servers():
	while True:
		time.sleep(5)
		for i in range(0, max_server_count):
			if not is_server_alive[i]:
				try:
					server_sockets[i].connect(server_addresses[i])
					is_server_alive[i]=True
					print('New server {0}has connected'.format(server_addresses[i]))
				except Exception as e:
					#print('{0} from adress {1}'.format(e, server_addresses[i]))
					is_server_alive[i]=False

def start_client():
	initialize_sockets()
	poll_thread = threading.Thread(target=poll_servers)
	send_request_thread = threading.Thread(target=handle_request_to_server)
	poll_thread.start()
	send_request_thread.start()

	poll_thread.join()
	send_request_thread.join()

start_client()


