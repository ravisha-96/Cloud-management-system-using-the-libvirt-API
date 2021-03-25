from __future__ import print_function
import sys
import libvirt
import time
from xml.dom import minidom

def get_guest_time(dom):
	stats = dom.getCPUStats(True)
	cpu_time = stats[0]['cpu_time']/ 1000000000.
	system_time = stats[0]['system_time']/ 1000000000
	user_time = stats[0]['user_time']/ 1000000000.
	guest_time= cpu_time - (system_time+user_time)
	return guest_time

def get_cpu_utilization(dom):
	guest_time1 = get_guest_time(dom)
	print("guest_time1 : ", guest_time1)
	dt = 15.
	time.sleep(15)
	guest_time2 = get_guest_time(dom)
	print("guest_time2 : ", guest_time2)
	return 100*((guest_time2-guest_time1)/dt)

def connect_to_qemu():
	conn = libvirt.open('qemu:///system')
	if conn == None:
	    print('Failed to open connection to qemu:///system', file=sys.stderr)
	    exit(1)
	return conn

def connect_to_domain(conn, domain_name):
	dom = conn.lookupByName(domain_name)
	if dom == None:
	    print('Failed to get the domain object', file=sys.stderr)
	    return -1
	return dom

def readConfig(filpath):
	with open(filpath, 'r') as config_file:
		config = config_file.read()
	return config

def createNewDomain(conn):
	xmlconfig = readConfig('./xml_config.txt')
	dom = conn.defineXML(xmlconfig)
	if dom == None:
	    print('Failed to define a domain from an XML definition.', file=sys.stderr)
	    exit(1)

	if dom.create() < 0:
	    print('Can not boot guest domain.', file=sys.stderr)
	    exit(1)

	print('Guest '+dom.name()+' has booted', file=sys.stderr)
	return dom


def monitor():
	conn = connect_to_qemu()
	print("connection to qemu has been established")
	dom = connect_to_domain(conn, 'generic2')
	thresold = 65
	print(get_cpu_utilization(dom))
	while True:
		cpu_utilization = get_cpu_utilization(dom)
		print(cpu_utilization)
	
	# if cpu_utilization > thresold:
	# 	dom2 = createNewDomain(conn)
	#socket on the newly created domain should be registered to the client
	conn.close()
	
monitor()
#print(readConfig('./xml_config.txt'))
