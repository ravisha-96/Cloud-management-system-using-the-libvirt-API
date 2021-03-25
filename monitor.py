from __future__ import print_function
import sys
import libvirt
import time

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
	dt = 5.
	time.sleep(5)
	guest_time2 = get_guest_time(dom)
	print("guest_time2 : ", guest_time2)
	return 100*((guest_time2-guest_time1)/dt)

def low_mode():
	return "low"

def high_mode():
	return "high"

def resumeExtraVM():
	return "resumed"

def monitor():
	return True

conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)
print("connection to qemu has been established")
host = conn.getHostname()
print('Hostname: '+host)

# vcpus = conn.getMaxVcpus(None)
# print('Maximum support virtual CPUs: '+str(vcpus))

# nodeinfo = conn.getInfo()
# print('Model: '+str(nodeinfo[0]))
# print('Memory size: '+str(nodeinfo[1])+'MB')
# print('Number of CPUs: '+str(nodeinfo[2]))
# print('MHz of CPUs: '+str(nodeinfo[3]))
# print('Number of NUMA nodes: '+str(nodeinfo[4]))
# print('Number of CPU sockets: '+str(nodeinfo[5]))
# print('Number of CPU cores per socket: '+str(nodeinfo[6]))
# print('Number of CPU threads per core: '+str(nodeinfo[7]))

# numnodes = nodeinfo[4]
# memlist = conn.getCellsFreeMemory(0, numnodes)
# cell = 0
# for cellfreemem in memlist:
#     print('Node '+str(cell)+': '+str(cellfreemem)+' bytes free memory')
#     cell += 1

# print('Virtualization type: '+conn.getType())

# ver = conn.getVersion()
# print('Version: '+str(ver))

# ver = conn.getLibVersion();
# print('Libvirt Version: '+str(ver));

# uri = conn.getURI()
# print('Canonical URI: '+uri)

# print('Connection is encrypted: '+str(conn.isEncrypted()))

# print('Connection is secure: '+str(conn.isSecure()))

# alive = conn.isAlive()
# print("Connection is alive = " + str(alive))

# mem = conn.getFreeMemory()
# print("Free memory on the node (host) is " + str(mem) + " bytes.")

# buf = conn.getMemoryParameters()
# for parm in buf:
#     print(parm)

# buf = conn.getMemoryStats(libvirt.VIR_NODE_MEMORY_STATS_ALL_CELLS)
# for parm in buf:
#     print(parm)

# model = conn.getSecurityModel()
# print(model[0] + " " + model[1])

# xmlInfo = conn.getSysinfo()
# print(xmlInfo)

# map = conn.getCPUMap()
# print("CPUs: " + str(map[0]))
# print("Available: " + str(map[1]))

# stats = conn.getCPUStats(0)
# print(stats)
# print("kernel: " + str(stats['kernel']))
# print("idle:   " + str(stats['idle']))
# print("user:   " + str(stats['user']))
# print("iowait: " + str(stats['iowait']))

# models = conn.getCPUModelNames('x86_64')
# for model in models:
#     print(model)

# domainName = 'rshankar_server'
# dom = conn.lookupByID(6)
# if dom == None:
#     print('Failed to get the domain object', file=sys.stderr)
# else:
# 	print(dom)

#getting the domain id's

domainIDs = conn.listDomainsID()
# if domainIDs == None:
#     print('Failed to get a list of domain IDs', file=sys.stderr)
# print("Active domain IDs:")
# if len(domainIDs) == 0:
#     print('  None')
# else:
#     for domainID in domainIDs:
#         print('  '+str(domainID))
print(domainIDs)
domainNames = conn.listDefinedDomains()
print(domainNames)
domains = conn.listAllDomains(0)
if len(domains) != 0:
    for domain in domains:
        print('  '+domain.name())

domName = 'generic'
dom = conn.lookupByName(domName)
if dom == None:
    print('Failed to find the domain '+domName, file=sys.stderr)
    exit(1)

id = dom.ID()
if id == -1:
    print('The domain is not running so has no ID.')
else:
    print('The ID of the domain is ' + str(id))



domainID=6
dom = conn.lookupByID(domainID)
dom = conn.lookupByName('generic')
if dom == None:
    print('Failed to get the domain object', file=sys.stderr)
print(dom)

stats = dom.getCPUStats(True)
print(stats)
print('cpu_time:    '+str(stats[0]['cpu_time']/ 1000000000.))
print('system_time: '+str(stats[0]['system_time']/ 1000000000.))
print('user_time:   '+str(stats[0]['user_time']/ 1000000000.))


# cpu_stats = dom.getCPUStats(False)
# print(cpu_stats)
# for (i, cpu) in enumerate(cpu_stats):
#    print('CPU '+str(i)+' Time: '+str(cpu['cpu_time'] / 1000000000.))
#    print('\t vcpu_time \t' + str(cpu['vcpu_time']/1000000000.))

print(get_cpu_utilization(dom))
conn.close()
exit(0)