from __future__ import print_function
import sys
import libvirt
import time
from xml.dom import minidom
import threading

class Monitor:
	def __init__(self):
		self.conn = None;
		self.cpu_utilization = 0
		self.domain_names = ['generic']
		self.dom_objects = list()
		self.is_scaled = False
		self.thresold = 65
		
	def connect_to_qemu(self):
		self.conn = libvirt.open('qemu:///system')
		if self.conn == None:
		    print('Failed to open connection to qemu:///system', file=sys.stderr)
		    exit(1)
	
	def connect_to_domain(self,domain_name):
		dom = self.conn.lookupByName(domain_name)
		if dom == None:
		    print('Failed to get the domain object', file=sys.stderr)
		    return -1
		return dom

	def get_guest_time(self, dom):
		stats = dom.getCPUStats(True)
		cpu_time = stats[0]['cpu_time']/ 1000000000.
		system_time = stats[0]['system_time']/ 1000000000
		user_time = stats[0]['user_time']/ 1000000000.
		guest_time= cpu_time - (system_time+user_time)
		return guest_time

	def get_cpu_utilization(self, dom):
		guest_time1 = self.get_guest_time(dom)
		print("\nguest_time1 : ", guest_time1)
		dt = 15.
		time.sleep(15)
		guest_time2 = self.get_guest_time(dom)
		print("guest_time2 : ", guest_time2)
		return 100*((guest_time2-guest_time1)/dt)

	def monitor(self):
		#Connect to the first domain and monitor the cpu_utilization of the first domain
		dom = self.connect_to_domain(self.domain_names[0])
		self.dom_objects.append(dom)

		while(True and self.cpu_utilization < self.thresold):
			self.cpu_utilization = self.get_cpu_utilization(dom)
			print('{0} cpu_utilization : {1}'.format(self.domain_names[0], self.cpu_utilization ))
			#How to handle(display) the cpu utilization of the two domain_names
		self.handle_upscaling()
		while(True):
			for i in range(0, len(self.dom_objects)):
				self.cpu_utilization = self.get_cpu_utilization(self.dom_objects[i])
				print('{0} cpu_utilization: {1}'.format(self.domain_names[i], self.cpu_utilization ))

	def readConfig(self, filpath):
		with open(filpath, 'r') as config_file:
			config = config_file.read()
		return config

	def create_and_run_new_domain(self):
		xmlconfig = self.readConfig('./xml_config_generic2.txt')
		dom = self.conn.defineXML(xmlconfig)
		if dom == None:
		    print('Failed to define a domain from an XML definition.', file=sys.stderr)
		    exit(1)

		if dom.create() < 0:
		    print('Can not boot guest domain.', file=sys.stderr)
		    exit(1)

		print('Guest '+dom.name()+' has booted', file=sys.stderr)
		return dom


	def handle_upscaling(self):
		print("Handling upscaling")
		self.domain_names.append('generic2')
		self.is_scaled = True
		new_dom = self.create_and_run_new_domain()
		self.dom_objects.append(new_dom)


	def kick_off(self):
		self.connect_to_qemu()
		print("qemu connected")
		self.monitor()
		self.conn.close()
		print("done")

monObj = Monitor()
monObj.kick_off()


# def handle_cpu_utilization(self):
# 	#Connect to the first domain and monitor the cpu_utilization of the first domain
# 	dom = self.connect_to_domain(self.domain_names[0])
# 	self.dom_objects.append(dom)
# 	while(True && self.is_scaled):
# 		self.cpu_utilization = self.get_cpu_utilization(dom)
# 		print(f'{0} cpu_utilization : {1}'.format(domain_names[0], self.cpu_utilization ))
# 		#How to handle(display) the cpu utilization of the two domain_names
# 	while(True):
# 		for i in range(0, len(self.dom_objects)):
# 			self.cpu_utilization = self.get_cpu_utilization(self.dom_objects[i])
# 			print('{0} cpu_utilization: {1}'.format(domain_names[1], self.cpu_utilization ))
