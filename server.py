# first of all import the socket library 
import socket		
import config
import threading

from common import mode

def compute(number):
	a =1;
	b=1;
	c=0;
	while c<number:
		d = a+b
		a = b
		b = d
		c = c+1
		print(b)
	return b


# next create a socket object 
s = socket.socket()		
s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 ) 
print ("Socket successfully created") 

port = 12346				

s.bind(('', port))		 
print ("socket binded to %s" %(port)) 

# put the socket into listening mode 
s.listen(5)	 
print ("socket is listening")			 


# Establish connection with client.
c, addr = s.accept()	 
print ('Got connection from', addr )  
# send a thank you message to the client. 
c.send('Thank you for connecting') 	
i=0
while i<5: 
	data = c.recv(1024)
	ans = compute(int(data))
	print(data)
	i = i+1
	c.send(str(ans))
	# Close the connection with the client 
c.close() 
