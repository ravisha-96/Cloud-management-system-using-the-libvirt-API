import socket
import config
import threading
import time
import sys

mode = None
while True:
	with open('common.txt', 'r') as f:
		mode = f.read()
	print(mode)
	time.sleep(5)
  
Create a socket object  
s = socket.socket()          
s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 ) 
# Define the port on which you want to connect
server_addresses = [('192.168.122.55', 12345), ('192.168.122.56', 12346)]  
port = 12345          
# mode = "high"
# connect to the server on local computer  
s.connect(('192.168.122.56', port))  
i=0
while True:  
	print("start")
	with open('common.txt', 'r') as f:
		mode = f.read()
	print(mode)
	if mode == "high":
		s.send("1000")
	elif mode == "low":
		s.send('320')
		time.sleep(1)
	i=i+1
	s.recv(1024)
	print("ans received")

	#print (s.recv(1024) ) 
	# close the connection  
s.close()