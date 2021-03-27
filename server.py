import socket
import threading
import string
import random
import datetime

def toString(List):
	return ''.join(List)

def permute(a, start, end):
	if start==end:
		toString(a)
		return
	else:
		for i in range(start, end+1):
			a[start], a[i] = a[i], a[start]
			permute(a, start+1, end)
			a[start], a[i] = a[i], a[start]

def compute(n):
	#print(datetime.datetime.now())
	res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
	res = list(res)
	permute(res, 0, n-1)
	#print(datetime.datetime.now())
	return "done"

#next create a socket object
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("socket successfully created")
port = 12346
s.bind('', port)
print("socket binded to %s"%(port))

#put the socket i listening mode
s.listen(5)
print("socket is listening")

#Establish connection with client
c, addr = s.accept()
print('Got connection from addr', addr)

while True:
	data = c.recv(1024).decode('utf-8')
	ans = compute(int(data))
	print(ans)
	c.send(bytes(ans, 'utf-8'))
c.close()



